# Secret Service Module

A centralized secret management system with in-memory storage, master password protection,
and encryption using Qt's cryptographic classes.

Example usage:
```cpp
#include "secret_service.h"

// Initialize with master password
SecretService* service = SecretService::getInstance();
service->authenticate("master_password_123");

// Create secrets
service->createSecret("github", "username", "myuser");
service->createSecret("github", "token", "ghp_abc123");

// Read secrets
QString username = service->readSecret("github", "username");
QString token = service->readSecret("github", "token");

// List services
QStringList services = service->listServices();

// Update secret
service->updateSecret("github", "token", "ghp_newtoken456");

// Delete secret
service->deleteSecret("github", "username");
```

## Implementation Structure

### Secret Class (`secret.h` / `secret.cpp`)

```cpp
class Secret {
public:
    QString name;
    QByteArray value;
    QString type;
    qint64 createdAt;
    qint64 updatedAt;
    
    Secret(const QString& name, const QByteArray& value, const QString& type);
};
```

### ServiceSecrets Class (`service_secrets.h` / `service_secrets.cpp`)

```cpp
class ServiceSecrets {
public:
    QString serviceName;
    QMap<QString, Secret> secrets;
    qint64 createdAt;
    qint64 updatedAt;
    
    ServiceSecrets(const QString& serviceName);
};
```

### SecretRepository Class (`secret_repository.h` / `secret_repository.cpp`)

Repository for handling CRUD operations on secrets in memory.

Methods:
- `void createSecret(const QString& serviceName, const QString& fieldName, const QVariant& value)`
- `QByteArray readSecret(const QString& serviceName, const QString& fieldName) const`
- `void updateSecret(const QString& serviceName, const QString& fieldName, const QVariant& value)`
- `void deleteSecret(const QString& serviceName, const QString& fieldName)`
- `QStringList listServices() const`
- `ServiceSecrets* getServiceSecrets(const QString& serviceName) const`
- `void clearAll()`

### SecretFactory Class (`secret_factory.h` / `secret_factory.cpp`)

Factory for creating Secret instances with timestamps.

Static methods:
- `Secret createSecret(const QString& name, const QVariant& value, const QString& type = QString())`
- `Secret createPasswordSecret(const QString& name, const QString& password)`
- `Secret createTokenSecret(const QString& name, const QString& token)`

### Seeder Class (`seeder.h` / `seeder.cpp`)

Seeder class to populate the repository with sample secrets for testing/demo.

Methods:
- `void seedSampleData()`
- `void seedCustomData(const QMap<QString, QMap<QString, QVariant>>& data)`

### MigrationManager Class (`migration_manager.h` / `migration_manager.cpp`)

Manager for initializing and resetting the repository structure.

Methods:
- `void initialize()`
- `void reset()`
- `void resetAndSeed(Seeder* seeder)`

### SecretService Class (`secret_service.h` / `secret_service.cpp`)

Main service class managing master password, encryption, and CRUD operations.

Uses Qt's cryptographic classes:
- `QCryptographicHash` for password hashing
- `QAESEncryption` or `QCA` (Qt Cryptographic Architecture) for encryption
- `QByteArray` for binary data handling

Methods:
- `bool authenticate(const QString& masterPassword)`
- `void createSecret(const QString& serviceName, const QString& fieldName, const QVariant& value)`
- `QString readSecret(const QString& serviceName, const QString& fieldName) const`
- `void updateSecret(const QString& serviceName, const QString& fieldName, const QVariant& value)`
- `void deleteSecret(const QString& serviceName, const QString& fieldName)`
- `QStringList listServices() const`
- `bool isAuthenticated() const`
- `void logout()`

Properties:
- `int expiryMinutes` (default: 5)
- Session expiry tracking

### Singleton Pattern

Use singleton pattern for global service instance:

```cpp
class SecretService {
public:
    static SecretService* getInstance(int expiryMinutes = 5);
    static void resetInstance();
    
private:
    static SecretService* instance;
    SecretService(int expiryMinutes);
};
```

## Encryption Implementation

Use Qt's cryptographic capabilities:
- `QCryptographicHash` with SHA-256 for password hashing
- `QCA` (Qt Cryptographic Architecture) for AES encryption, or
- `QAESEncryption` for simpler AES encryption
- `QRandomGenerator` for generating salts

## Project Structure

```
app/
├── services/
│   ├── secret_service/
│   │   ├── secret.h
│   │   ├── secret.cpp
│   │   ├── service_secrets.h
│   │   ├── service_secrets.cpp
│   │   ├── secret_repository.h
│   │   ├── secret_repository.cpp
│   │   ├── secret_factory.h
│   │   ├── secret_factory.cpp
│   │   ├── seeder.h
│   │   ├── seeder.cpp
│   │   ├── migration_manager.h
│   │   ├── migration_manager.cpp
│   │   ├── secret_service.h
│   │   └── secret_service.cpp
```

## CMakeLists.txt Updates

Add Qt cryptographic modules:

```cmake
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS 
    Widgets 
    Core
)

# If using QCA (optional, more advanced)
# find_package(QCA)
```

## Dependencies

- Qt Core module (for `QCryptographicHash`, `QByteArray`, `QString`, etc.)
- Optional: QCA (Qt Cryptographic Architecture) for advanced encryption
- Or: QAESEncryption library for AES encryption

## Notes

- All timestamps use `qint64` (milliseconds since epoch) or `QDateTime`
- Use `QByteArray` for binary data (encrypted values)
- Use `QString` for text data
- Use `QVariant` for flexible value types
- Memory management: Use Qt's parent-child relationship or smart pointers
- Thread safety: Consider `QMutex` if accessed from multiple threads
