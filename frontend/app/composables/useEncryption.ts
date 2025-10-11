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
    const bytes = buffer instanceof Uint8Array ? buffer : new Uint8Array(buffer);
    let binary = '';
    for (let i = 0; i < bytes.byteLength; i++) {
      binary += String.fromCharCode(bytes[i]);
    }
    return btoa(binary);
  };

  // Criptografar texto usando Web Crypto API
  const encryptText = async (text: string, publicKeyBase64: string): Promise<{ encryptedBlob: string; wrappedKey: string }> => {
    try {
      console.log('🔐 Iniciando criptografia...');

      // 1. Gerar DEK (Data Encryption Key) aleatória para AES-GCM
      const dek = crypto.getRandomValues(new Uint8Array(32));
      console.log('📦 DEK gerada:', dek.length, 'bytes');

      // 2. Importar chave pública RSA do servidor
      const publicKeyData = base64ToArrayBuffer(publicKeyBase64);
      const publicKey = await crypto.subtle.importKey(
        'spki',
        publicKeyData,
        {
          name: 'RSA-OAEP',
          hash: 'SHA-256'
        },
        false,
        ['encrypt']
      );

      // 3. Cifrar DEK com RSA (wrapping)
      const wrappedKey = await crypto.subtle.encrypt(
        { name: 'RSA-OAEP' },
        publicKey,
        dek
      );
      console.log('🔑 DEK cifrada com RSA:', wrappedKey.byteLength, 'bytes');

      // 4. Gerar IV (Initialization Vector) para AES-GCM
      const iv = crypto.getRandomValues(new Uint8Array(12));
      console.log('🎲 IV gerado:', iv.length, 'bytes');

      // 5. Importar DEK para uso com AES-GCM
      const aesKey = await crypto.subtle.importKey(
        'raw',
        dek,
        { name: 'AES-GCM' },
        false,
        ['encrypt']
      );

      // 6. Cifrar texto com AES-GCM
      const textEncoder = new TextEncoder();
      const textData = textEncoder.encode(text);
      
      const encryptedData = await crypto.subtle.encrypt(
        {
          name: 'AES-GCM',
          iv: iv,
          additionalData: textEncoder.encode('SIA-Denuncia')
        },
        aesKey,
        textData
      );
      console.log('📝 Texto cifrado com AES-GCM:', encryptedData.byteLength, 'bytes');

      // 7. Combinar IV + dados cifrados em um único blob
      const combinedBlob = new Uint8Array(iv.length + encryptedData.byteLength);
      combinedBlob.set(iv, 0);
      combinedBlob.set(new Uint8Array(encryptedData), iv.length);

      // 8. Converter para Base64 para envio
      const encryptedBlobBase64 = arrayBufferToBase64(combinedBlob);
      const wrappedKeyBase64 = arrayBufferToBase64(wrappedKey);

      console.log('✅ Criptografia concluída com sucesso!');
      console.log('📊 Estatísticas:', {
        textoOriginal: text.length,
        blobCifrado: encryptedBlobBase64.length,
        chaveEmbrulhada: wrappedKeyBase64.length
      });
      
      return {
        encryptedBlob: encryptedBlobBase64,
        wrappedKey: wrappedKeyBase64
      };

    } catch (error) {
      console.error('❌ Erro na criptografia:', error);
      throw new Error(`Falha na criptografia: ${error}`);
    }
  };

  return {
    encryptText
  };
};