#include <iostream>
#include <limits>
#include <stack>
#include <unordered_map>
#include <unordered_set>

typedef struct Dir {
    int fileSize = 0; // Excludes files in subdirectories
    std::unordered_map<std::string, Dir*> subDirs;
} Dir;

int collectSizes(Dir* dir, std::unordered_multiset<int>& sizes) {
    int totalSize = dir->fileSize;
    for (const auto& [_, subDir] : dir->subDirs) {
        totalSize += collectSizes(subDir, sizes);
    }
    sizes.insert(totalSize);
    return totalSize;
}

int main() {
    std::stack<Dir*> filePath;
    Dir* rootDir = new Dir;
    Dir* currDir = rootDir;

    std::cin.ignore(); // Ignore first "$"
    std::string command;
    while (std::cin >> command) {
        if (command == "cd") {
            std::string directory;
            std::cin >> directory;
            if (directory == "/") {
                filePath = {};
                currDir = rootDir;
            } else if (directory == "..") {
                currDir = filePath.top();
                filePath.pop();
            } else {
                filePath.push(currDir);
                auto it = currDir->subDirs.find(directory);
                if (it == currDir->subDirs.end()) {
                    Dir* newDir = new Dir();
                    currDir->subDirs[directory] = newDir;
                    currDir = newDir;
                } else {
                    currDir = it->second;
                }
            }
            std::cin.ignore(2); // Ignore "\n$"
        } else { // "ls"
            int totalFileSize = 0;
            std::string token;
            while ((std::cin >> token) && token != "$") {
                if (token != "dir") {
                    totalFileSize += stoi(token);
                }
                // Ignore file/directory name
                std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
            }
            currDir->fileSize = totalFileSize;
        }
    }

    std::unordered_multiset<int> sizes;
    int totalSize = collectSizes(rootDir, sizes);
    int totalSmallSizes = 0; // Part 1
    int minDeletionSize = INT32_MAX; // Part 2
    int requiredDeletionSize = totalSize - 40000000;
    for (int size : sizes) {
        if (size <= 100000) {
            totalSmallSizes += size;
        }
        if (size >= requiredDeletionSize) {
            minDeletionSize = std::min(minDeletionSize, size);
        }
    }
    std::cout << totalSmallSizes << "\n";
    std::cout << minDeletionSize << "\n";
}
