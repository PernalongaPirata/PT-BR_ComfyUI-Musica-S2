class YuE2AudioDurationMatch:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio": ("AUDIO",),
                # Adiciona a entrada para segundos extras, padrão é 0
                "extra_seconds": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 3600.0, "step": 1.0}),
            }
        }

    # Retorna tanto Float (exato) quanto Int (arredondado) para garantir compatibilidade
    RETURN_TYPES = ("FLOAT", "INT")
    RETURN_NAMES = ("duration_float", "duration_int")
    FUNCTION = "get_duration"
    CATEGORY = "YuE2 Music"

    def get_duration(self, audio, extra_seconds):
        # O ComfyUI passa o áudio como um dicionário contendo o tensor do waveform e a taxa de amostragem
        waveform = audio.get("waveform")
        sample_rate = audio.get("sample_rate")

        if waveform is None or sample_rate is None:
            raise ValueError("Formato de áudio inválido. Certifique-se de conectar a saída correta de áudio (AUDIO).")

        # O formato do waveform geralmente é [batch, channels, samples]
        # Pegamos o tamanho da última dimensão, que representa a quantidade total de frames/samples de áudio
        num_samples = waveform.shape[-1]
        
        # Faz a conversão para float para obter os segundos exatos de duração original
        base_duration = float(num_samples) / float(sample_rate)
        
        # Soma a duração base com os segundos extras solicitados pelo usuário
        duration_float = base_duration + float(extra_seconds)
        duration_int = int(duration_float)

        return (duration_float, duration_int)

# Registra o nó no ComfyUI
NODE_CLASS_MAPPINGS = {
    "YuE2AudioDurationMatch": YuE2AudioDurationMatch
}

# Nome amigável que vai aparecer no menu de busca de nós
NODE_DISPLAY_NAME_MAPPINGS = {
    "YuE2AudioDurationMatch": "YuE2 Music: Match Reference Duration"
}
