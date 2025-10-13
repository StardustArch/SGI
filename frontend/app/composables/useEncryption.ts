export const useEncryption = () => {
  // Converter Base64 para ArrayBuffer
  const base64ToArrayBuffer = (base64: string): ArrayBuffer => {
    const binaryString = atob(base64);
    const bytes = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }
    return bytes.buffer;
  };

  // Converter ArrayBuffer para Base64
  const arrayBufferToBase64 = (buffer: ArrayBuffer | Uint8Array): string => {
    const bytes =
      buffer instanceof Uint8Array ? buffer : new Uint8Array(buffer);
    let binary = "";
    for (const b of bytes) {
      binary += String.fromCharCode(b);
    }

    return btoa(binary);
  };

  const encryptText = async (
    text: string,
    publicKeyBase64: string
  ): Promise<{ encryptedBlob: string; wrappedKey: string }> => {
    try {
      console.log("🔐 Iniciando criptografia...");
      console.log("Texto original:", text);
      console.log("Tamanho do texto:", text.length, "caracteres");

      // 1. Gerar DEK (Data Encryption Key)
      const dek = crypto.getRandomValues(new Uint8Array(32));
      console.log("📦 DEK gerada:", dek.length, "bytes");

      // 2. Importar chave pública RSA
      const publicKeyData = base64ToArrayBuffer(publicKeyBase64);
      console.log(
        "🔑 Chave pública (Base64):",
        publicKeyBase64.length,
        "caracteres"
      );

      const publicKey = await crypto.subtle.importKey(
        "spki",
        publicKeyData,
        {
          name: "RSA-OAEP",
          hash: { name: "SHA-256" },
        },
        false,
        ["encrypt"]
      );
      console.log("✅ Chave pública importada");

      // 3. Cifrar DEK com RSA (wrapping)
      const wrappedKey = await crypto.subtle.encrypt(
        { name: "RSA-OAEP" },
        publicKey,
        dek
      );
      console.log("🔑 DEK cifrada com RSA:", wrappedKey.byteLength, "bytes");

      // 4. Gerar IV para AES-GCM
      const iv = crypto.getRandomValues(new Uint8Array(12));
      console.log("🎲 IV gerado:", iv.length, "bytes");

      // 5. Importar DEK para uso com AES-GCM
      const aesKey = await crypto.subtle.importKey(
        "raw",
        dek,
        { name: "AES-GCM" },
        false,
        ["encrypt"]
      );
      console.log("✅ Chave AES importada");

      // 6. Cifrar texto com AES-GCM
      const textEncoder = new TextEncoder();
      const textData = textEncoder.encode(text);
      console.log("📝 Texto codificado:", textData.length, "bytes");

      const encryptedData = await crypto.subtle.encrypt(
        {
          name: "AES-GCM",
          iv: iv,
        },
        aesKey,
        textData
      );
      console.log(
        "📝 Texto cifrado com AES-GCM:",
        encryptedData.byteLength,
        "bytes"
      );

      // 7. Combinar IV + dados cifrados
      const combinedBlob = new Uint8Array(iv.length + encryptedData.byteLength);
      combinedBlob.set(iv, 0);
      combinedBlob.set(new Uint8Array(encryptedData), iv.length);
      console.log(
        "📦 Blob combinado (IV + encrypted):",
        combinedBlob.length,
        "bytes"
      );

      // 8. Converter para Base64
      const encryptedBlobBase64 = arrayBufferToBase64(combinedBlob);
      const wrappedKeyBase64 = arrayBufferToBase64(wrappedKey);

      console.log("✅ Criptografia concluída com sucesso!");
      console.log("📊 Estatísticas finais:");
      console.log(
        "   - EncryptedBlob Base64:",
        encryptedBlobBase64.length,
        "caracteres"
      );
      console.log(
        "   - WrappedKey Base64:",
        wrappedKeyBase64.length,
        "caracteres"
      );
      console.log(
        "   - Tamanho esperado do blob:",
        Math.ceil((combinedBlob.length * 4) / 3),
        "caracteres Base64 (approx)"
      );

      return {
        encryptedBlob: encryptedBlobBase64,
        wrappedKey: wrappedKeyBase64,
      };
    } catch (error) {
      console.error("❌ Erro na criptografia:", error);
      throw new Error(`Falha na criptografia: ${error}`);
    }
  };

  return {
    encryptText,
  };
};
