from transformers import AutoTokenizer, AutoModelForCausalLM


class Generativo:

    # Constructor de la clase
    def __init__(self, model, tokenizer):
        self.model = AutoModelForCausalLM.from_pretrained(model)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer)

    # Método destructor
    def __del__(self):
        self.model = ""  # el método del no siempre garantiza 100% la eliminación del objeto
        self.tokenizer = ""

    def get_model(self):
        return self.model

    def set_model(self, new_model):
        self.model = AutoModelForCausalLM.from_pretrained(new_model)

    def get_tokenizer(self):
        return self.tokenizer

    def set_tokenizer(self, new_tokenizer):
        self.tokenizer = new_tokenizer

    def gen_frase(self, input_text):
        aux_text = "<SF>" + input_text
        batch = self.tokenizer(aux_text, return_tensors='pt')
        # batch = batch.to('cuda')
        # model = model.to('cuda')
        # with torch.cuda.amp.autocast():
        output_tokens = self.model.generate(**batch,
                                            max_new_tokens=15,
                                            # eos_token_id=30, # para pictos_gpt2_full_ft
                                            eos_token_id=50258,  # para prueba [50258, 50257]
                                            num_beams=3,
                                            no_repeat_ngram_size=2,
                                            num_return_sequences=3,
                                            )

        frases = []
        for i, out_token in enumerate(output_tokens):
            frases.append(self.tokenizer.decode(output_tokens[i], skip_special_tokens=False))
            # print("{}: {}".format(i, tokenizer.decode(output_tokens[i], skip_special_tokens=False)))
        return frases
