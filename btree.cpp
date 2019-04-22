#include <iostream>
#include <stdio.h>
#include <string>

using namespace std;
#define T 5
struct Node;

FILE *tree;
int currentFilePos = 0;

int writeNodeAtNextPosAvaible(Node &);

void writeNodeAtPosition(Node &n, int pos);

Node *readNodeAtPosition(int pos);

Node &getRoot();

struct Node {
    int size;
    int leaf;
    int pos;
    int parentPos;
    int keys[2 * T - 1];
    int childPositions[2 * T];

    Node() {
        size = 0;
        leaf = 0;
        pos = 0;
        parentPos = -1;
        for (int i = 0; i < 2 * T; i++) {
            childPositions[i] = -1;
        }
    }

    /*
     * Beacuse all data is being loaded from hard drive sometimes it is needed to retrive data once again after rotate for example
     */
    void reload() {
        Node *data = readNodeAtPosition(pos);
        size = data->size;
        leaf = data->leaf;
        parentPos = data->parentPos;
        for (int i = 0; i < 2 * T - 1; i++) {
            keys[i] = data->keys[i];
        }
        for (int i = 0; i < 2 * T; i++) {
            childPositions[i] = data->childPositions[i];
        }
        delete data;
    }

    /*
     * Operation without checks, keeps order in node, increament the counter
     */

    int addToKeys(int value) {
        int tmp;
        int pos = -1;
        for (int i = 0; i < size; i++) {
            if (value < keys[i]) {
                tmp = keys[i];
                keys[i] = value;
                pos = i;
                break;
            }
        }
        if (pos < 0) {
            pos = size;
            keys[size] = value;
        } else {
            for (int j = pos + 1; j < 2 * T - 1; j++) {
                int tmp2 = keys[j];
                keys[j] = tmp;
                tmp = tmp2;
            }
        }
        size++;
        return pos;
    }

    /*
     * Operation without checks, keeps order in node, decreament the counter
     */
    int removeFromKeys(int value) {
        int delPos = -1;
        for (int i = 0; i < size; i++) {
            if (keys[i] == value) {
                delPos = i;
                break;
            }
        }
        if (delPos >= 0) {
            for (int i = delPos; i < size - 1; i++) {
                keys[i] = keys[i + 1];
            }
            size--;
        }
        return delPos;
    }

    /*
     * Returns right brother if brother is ready to share keys
     */

    Node *getRightBrother() {
        if (parentPos < 0) {
            return nullptr;
        } else {
            Node *parent = readNodeAtPosition(this->parentPos);
            int rightBrotherPos = -1;
            for (int i = 0; i < parent->size; i++) {
                if (parent->keys[i] > this->keys[this->size - 1]) {
                    rightBrotherPos = i;
                    break;
                }
            }
            if (rightBrotherPos >= 0) {
                Node *rightBrother = readNodeAtPosition(parent->childPositions[rightBrotherPos + 1]); //to check that
                delete parent;
                if (rightBrother->size < T) {
                    delete rightBrother;
                    return nullptr;
                } else {
                    return rightBrother;
                }
            } else {
                return nullptr;
            }
        }
    }


    /*
     * Returns left brother if brother is ready to share keys
     */

    Node *getLeftBrother() {
        if (parentPos < 0) {
            return nullptr;
        } else {
            Node *parent = readNodeAtPosition(this->parentPos);
            int leftBrotherPos = -1;
            for (int i = parent->size - 1; i >= 0; i--) {
                if (parent->keys[i] < this->keys[0]) {
                    leftBrotherPos = i;
                    break;
                }
            }
            if (leftBrotherPos >= 0) {
                Node *leftBrother = readNodeAtPosition(parent->childPositions[leftBrotherPos]);
                delete parent;
                if (leftBrother->size < T) {
                    delete leftBrother;
                    return nullptr;
                } else {
                    return leftBrother;
                }
            } else {
                return nullptr;
            }

        }
    }

    /*
     * If it is possible joins two childs and key at given key position, returns new created node
     */

    Node *joinAtKeyPos(int p) {
        Node *leftJoin = readNodeAtPosition(this->childPositions[p]);
        Node *rightJoin = readNodeAtPosition(this->childPositions[p + 1]);
        if (leftJoin->size == T - 1 && rightJoin->size == T - 1) {
            Node *newNode = new Node();
            newNode->parentPos = this->pos;
            newNode->leaf = leftJoin->leaf;
            for (int i = 0; i < T - 1; i++) {
                newNode->addToKeys(leftJoin->keys[i]);
                newNode->addToKeys(rightJoin->keys[i]);
            }
            newNode->addToKeys(this->keys[p]);
            int newNodePos;
            if (this->size == 1) { //węzeł zostaje mianowany korzeniem
                newNodePos = 0;
                newNode->pos = 0;
                newNode->parentPos = -1;
                writeNodeAtPosition(*newNode, newNodePos);
            } else {
                newNodePos = writeNodeAtNextPosAvaible(*newNode);
            }
            if (!leftJoin->leaf) {
                for (int i = 0; i < T; i++) {
                    newNode->childPositions[i] = leftJoin->childPositions[i];
                    newNode->childPositions[i + T] = rightJoin->childPositions[i];
                }

                for (int i = 0; i <= 2 * T; i++) {
                    Node *child = readNodeAtPosition(newNode->childPositions[i]);
                    child->parentPos = newNodePos;
                    writeNodeAtPosition(*child, child->pos);
                }
                writeNodeAtPosition(*newNode, newNodePos);
            }
            for (int i = p; i < 2 * T - 1; i++) {
                this->childPositions[i] = this->childPositions[i + 1];
            }
            this->childPositions[p] = newNodePos;
            this->removeFromKeys(this->keys[p]);
            writeNodeAtPosition(*this, this->pos);
            writeNodeAtPosition(*newNode, newNodePos);
            return newNode;
        } else {
            return nullptr;
        }
    }

    /*
     * Rotate right to give (this) node extra key (with checks)
     */

    bool rotateRight() { //in prother perspective
        if (this->size != T - 1) return false; //rotate only if we have less than T elements
        Node *left = getLeftBrother();
        Node *parent = readNodeAtPosition(this->parentPos);
        if (left != nullptr) {
            int pPos = -1;
            for (int i = 0; i < parent->size; i++) {
                if (parent->keys[i] > left->keys[0] && parent->keys[i] < this->keys[0]) {
                    pPos = i;
                }
            }
            int pValue = parent->keys[pPos];
            parent->keys[pPos] = left->keys[left->size - 1];
            if (!this->leaf) {
                int leftChildPos = left->childPositions[left->size]; //most right leaf to be my most left leaf
                for (int i = 2 * T - 2; i >= 0; i--) {
                    this->childPositions[i + 1] = this->childPositions[i];
                }
                this->childPositions[0] = leftChildPos;
            }
            left->removeFromKeys(left->keys[left->size - 1]);
            this->addToKeys(pValue);
            writeNodeAtPosition(*left, left->pos);
            writeNodeAtPosition(*parent, parent->pos);
            writeNodeAtPosition(*this, this->pos);
            return true;
        } else {
            return false;
        }
    }

    /*
     * Rotate left to give (this) node extra key (with checks)
     */

    bool rotateLeft() {
        if (this->size != T - 1) return false; //rotate only if we have less than T elements
        Node *right = getRightBrother();
        Node *parent = readNodeAtPosition(this->parentPos);
        if (right != nullptr) {
            int pPos = -1;
            for (int i = 0; i < parent->size; i++) {
                if (parent->keys[i] < right->keys[0] && parent->keys[i] > this->keys[0]) {
                    pPos = i;
                }
            }
            int pValue = parent->keys[pPos];
            parent->keys[pPos] = right->keys[0];
            if (!this->leaf) {
                int rightChildPos = right->childPositions[0]; //most right leaf to be my most left leaf
                this->childPositions[this->size + 1] = rightChildPos;
                for (int i = 0; i < 2 * T - 1; i++) {
                    right->childPositions[i] = right->childPositions[i + 1];
                }
            }
            right->removeFromKeys(right->keys[0]);
            this->addToKeys(pValue);
            writeNodeAtPosition(*right, right->pos);
            writeNodeAtPosition(*parent, parent->pos);
            writeNodeAtPosition(*this, this->pos);
            return true;
        } else {
            return false;
        }
    }

    /*
     * Despite its name it returns most right node and in meantime fixes tree
     */

    Node *prevWithFix() {
        if (this->leaf) {
            return this;
        } else {
            if (rotateRight()) {
                return readNodeAtPosition(this->childPositions[this->size])->prevWithFix();
            } else {
                Node *fixNode = joinAtKeyPos(this->size - 1);
                if (fixNode != nullptr) {
                    return fixNode->prevWithFix();
                } else {
                    return readNodeAtPosition(this->childPositions[this->size])->prevWithFix();
                }
            }

        }
    }

    /*
     * Despite its name it returns most left node and in meantime fixes tree
     */

    Node *nextWithFix() {
        if (this->leaf) {
            return this;
        } else {
            if (rotateLeft()) {
                return readNodeAtPosition(this->childPositions[0])->prevWithFix();
            } else {
                Node *fixNode = joinAtKeyPos(0);
                if (fixNode != nullptr) {
                    return fixNode->prevWithFix();
                } else {
                    return readNodeAtPosition(this->childPositions[0])->prevWithFix();
                }
            }

        }
    }

    /*
     * Main feature of this project, deleting node from tree (we assume executing this on a root)
     */

    void removeElement(int value) {
        Node test = getRoot();
        if (leaf) {
            removeFromKeys(value);
            writeNodeAtPosition(*this, this->pos);
        } else {
            int delPos = -1;
            for (int i = 0; i < size; i++) {
                if (keys[i] == value) {
                    delPos = i;
                    break;
                }
            }
            if (delPos >= 0) {
                Node *child = readNodeAtPosition(this->childPositions[delPos]);
                if (child->rotateLeft()) {
                    child->removeElement(value);
                } else if (child->rotateRight()) {
                    this->reload();
                    Node *nextChild = child->prevWithFix();
                    int tmp = nextChild->keys[nextChild->size - 1];
                    nextChild->keys[nextChild->size - 1] = value;
                    this->keys[delPos] = tmp;
                    writeNodeAtPosition(*nextChild, nextChild->pos);
                    writeNodeAtPosition(*this, this->pos);
                    nextChild->removeElement(value);
                } else {
                    Node *newElement = this->joinAtKeyPos(delPos);
                    if (newElement != nullptr) {
                        newElement->removeElement(value);
                    } else {
                        Node *nextChild = child->prevWithFix();
                        int tmp = nextChild->keys[nextChild->size - 1];
                        nextChild->keys[nextChild->size - 1] = value;
                        this->keys[delPos] = tmp;
                        writeNodeAtPosition(*nextChild, nextChild->pos);
                        writeNodeAtPosition(*this, this->pos);
                        nextChild->removeElement(value);
                    }
                }
            } else {
                for (int i = 0; i < size; i++) {
                    if (this->keys[i] > value) {
                        delPos = i;
                        break;
                    }
                }
                if (delPos < 0) delPos = size;
                Node *child = readNodeAtPosition(this->childPositions[delPos]);
                if (child->rotateLeft() || child->rotateRight()) {
                    child->removeElement(value);
                } else {
                    Node *newElement = this->joinAtKeyPos(delPos);
                    if (newElement != nullptr) {
                        newElement->removeElement(value);
                    } else {
                        child->removeElement(value);
                    }
                }
            }
        }
    }

    /*
     * Second main feature, addding element to keys with all checks and spliting tree if possible (we assume executing this on a root)
     */
    void addElement(int value) {
        if (size == 2 * T - 1) {
            Node left;
            Node right;
            left.leaf = 1;
            right.leaf = 1;
            left.parentPos = this->parentPos < 0 ? this->pos : this->parentPos;
            right.parentPos = this->parentPos < 0 ? this->pos : this->parentPos;
            for (int i = 0; i < T; i++) {
                left.keys[i] = this->keys[i];
                right.keys[i] = this->keys[i + T];
            }
            right.size = T - 1;
            left.size = T - 1;
            if (!this->leaf) {
                left.leaf = 0;
                right.leaf = 0;
                for (int i = 0; i < T; i++) {
                    left.childPositions[i] = this->childPositions[i];
                    right.childPositions[i] = this->childPositions[i + T];
                }


            }
            int leftPos = writeNodeAtNextPosAvaible(left);
            int rightPos = writeNodeAtNextPosAvaible(right);

            if (!this->leaf) {
                for (int i = 0; i < T; i++) {
                    Node *leftChild = readNodeAtPosition(left.childPositions[i]);
                    Node *rightChild = readNodeAtPosition(right.childPositions[i]);
                    leftChild->parentPos = leftPos;
                    rightChild->parentPos = rightPos;
                    writeNodeAtPosition(*leftChild, leftChild->pos);
                    writeNodeAtPosition(*rightChild, rightChild->pos);
                }
            }
            this->leaf = 0;

            if (this->parentPos == -1) { //if node is root
                this->size = 1;
                this->keys[0] = this->keys[T - 1];
                this->childPositions[0] = leftPos;
                this->childPositions[1] = rightPos;
                for (int i = 2; i < 2 * T; i++) {
                    this->childPositions[i] = -1;
                }
            } else {
                Node *parent = readNodeAtPosition(this->parentPos);
                int upvalue = this->keys[T - 1];
                int insertedPos = parent->addToKeys(upvalue);

                parent->childPositions[insertedPos] = leftPos;

                for (int i = 2 * T - 1; i > insertedPos; i--) {
                    parent->childPositions[i] = parent->childPositions[i - 1];
                }

                parent->childPositions[insertedPos + 1] = rightPos;


                writeNodeAtPosition(*parent, parent->pos);
            }
            writeNodeAtPosition(*this, this->pos);
            if (value <= this->keys[T - 1]) {
                left.addElement(value);
            } else {
                right.addElement(value);
            }

        } else {
            if (leaf) {
                addToKeys(value);
                writeNodeAtPosition(*this, this->pos);
            } else {
                //insert value to correct subtree
                int subtreePos = this->size;
                for (int i = 0; i < this->size; i++) {
                    if (value < this->keys[i]) {
                        subtreePos = i;
                        break;
                    }
                }
                Node *subtree = readNodeAtPosition(this->childPositions[subtreePos]);
                subtree->addElement(value);
            }
        }
    }
};

const int nodeSize = sizeof(Node);

void writeNodeAtPosition(Node &n, int pos) {
    fseek(tree, (long) nodeSize * pos, SEEK_SET);
    fwrite(&n, nodeSize, 1, tree);
}

int writeNodeAtNextPosAvaible(Node &n) {
    n.pos = currentFilePos;
    fseek(tree, (long) nodeSize * currentFilePos, SEEK_SET);
    fwrite(&n, nodeSize, 1, tree);
    currentFilePos++;
    return currentFilePos - 1;
}

Node *readNodeAtPosition(int pos) {
    Node *n = new Node();
    fseek(tree, (long) nodeSize * pos, SEEK_SET);
    fread(n, nodeSize, 1, tree);
    return n;
}

Node &getRoot() {
    return *readNodeAtPosition(0);
}


std::ostream &operator<<(std::ostream &stream, const Node &node) {
    static int offset = 0;

    stream << string(offset, ' ') << "(";
    for (int i = 0; i < node.size; i++) {
        stream << node.keys[i] << " ";
    }
    if (node.leaf)
        return stream << ")" << endl;
    stream << ") is father of { \n";
    offset += 2;
    for (int i = 0; i <= node.size; i++) {
        if (node.childPositions[i] >= 0) {
            Node *child = readNodeAtPosition(node.childPositions[i]);
            stream << string(offset, ' ') << *child;
        }
    }
    offset -= 2;
    return stream << string(offset, ' ') << "} \n";
}


int main() {
    tree = fopen("btree.b", "w+");
    Node root;
    root.leaf = 1;
    root.size = 0;
    root.parentPos = -1;
    writeNodeAtNextPosAvaible(root);

    for (int i = 0; i < 500; i++) {
        getRoot().addElement(i * 10);
    }

    cout << getRoot() << endl;

    for (int i = 25; i >= 0; i--) {
        getRoot().removeElement(i * 10);
    }

    for (int i = 200; i < 300; i++) {
        getRoot().removeElement(i * 10);
    }

    cout << getRoot() << endl;
    fclose(tree);
}