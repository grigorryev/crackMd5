#ifndef COMMON_H
#define COMMON_H

#define OWNER_BYTES_LEN 32
#define USER_BYTES_LEN 32
#define FILEID_BYTES_LEN 16

#define MAX_BUFFER_LENGTH (128 - sizeof(uint))
#define MAX_PASSWORD_LENGTH (64-sizeof(uint))

typedef struct {
  uint size_bytes;
  char password[MAX_PASSWORD_LENGTH];
} password_t;

typedef struct {
  uint v[4];
} password_hash_t;

typedef struct {
  uint size;
  char buffer[MAX_BUFFER_LENGTH];
} buffer_t;

#endif // COMMON_H
