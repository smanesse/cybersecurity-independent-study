# Padded oracle

A padded oracle attack is possible when an application gives some indication when decrypting a cyphertext as to whether or not that ciphertext has valid padding. It abuse the use of PKCS7 padding commonly used by AES encryption.

To understand the attack, I used this article <https://robertheaton.com/2013/07/29/padding-oracle-attack/>. It explains it very well - here's a few big takeaways:
- The cyphertext is in specific block sizes, and each block is XORed with the decrypted next block to produce the final plaintext:
Let C1, C2 be ciphertext blocks 1 and 2, and let P2 be the plaintext of C2. I2 is the intermediate state between C2 and P2 - i.e. the private key is used to decrypt C2 and produces I2. Let ^ be the XOR operation. Let block 2 be the final block of the ciphertext.
P2 = I2 ^ C1, so P2[16] = I2[16] ^ C1[16].
There are two cases where the padding is correct: P2[16] is what it originally was, or P2[16] = 01. We know what value of C1[16] will produce the original value of P2[16] (that being C1[16]), so we can reverse engineer this process to choose a value of C1[16] such that there is valid padding (P2[16] = 01). By checking every value of the byte C1[16] (0-255) except the original C1[16], we can find a value _x_ such that 01 = I2[16] ^ x. Because of how XOR works, we can then extract the value of I2[16] = 01 ^ x. Once we have the value of I2[16], we can get the original value of P2[16] by the following:
P2[16] = I2[16] ^ C1[16].
P2[16] = (x ^ 01) ^ C1[16].
Since we have the values on the right side of the equation we can get P2[16].
To decrypt the rest of the blocks, we can extend the padding to 02, 02. We just need to remember the value of x[16] so we can force P2[16] to be 02. Now the only value that will give valid padding for C1[15] is one that produced P2[15] = 02. Repeat this pattern for every block, and the remove the block and continue.
