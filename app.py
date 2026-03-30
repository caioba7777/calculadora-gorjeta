from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = "segredo"


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        conta_str = request.form.get("conta", "").strip()
        pessoas_str = request.form.get("pessoas", "").strip()
        gorjeta_str = request.form.get("gorjeta", "").strip()

        erros = []

        if not conta_str:
            erros.append("O valor da conta é obrigatório.")
        if not pessoas_str:
            erros.append("A quantidade de pessoas é obrigatória.")
        if not gorjeta_str:
            erros.append("O percentual de gorjeta é obrigatório.")

        conta = None
        pessoas = None
        gorjeta = None

        if conta_str:
            try:
                conta = float(conta_str)
                if conta <= 0:
                    erros.append("O valor da conta deve ser maior que zero.")
            except ValueError:
                erros.append("O valor da conta deve ser numérico.")

        if pessoas_str:
            try:
                pessoas = int(pessoas_str)
                if pessoas <= 0:
                    erros.append("A quantidade de pessoas deve ser maior que zero.")
            except ValueError:
                erros.append("A quantidade de pessoas deve ser um número inteiro.")

        if gorjeta_str:
            try:
                gorjeta = float(gorjeta_str)
                if gorjeta < 0:
                    erros.append("O percentual de gorjeta deve ser maior ou igual a zero.")
            except ValueError:
                erros.append("O percentual de gorjeta deve ser numérico.")

        if erros:
            for erro in erros:
                flash(erro)
            return render_template("index.html")

        valor_gorjeta = round ( conta * (gorjeta / 100 ) ,2 )
        total = round (conta + valor_gorjeta, 2)
        por_pessoa = round ( total / max( pessoas ,1) ,2)

        if gorjeta < 5:
            classificacao = "Mão de vaca"
            cor = "danger"
        elif gorjeta <= 15:
            classificacao = "Legal"
            cor = "warning"
        else:
            classificacao = "Generoso"
            cor = "success"

        return render_template(
            "resultado.html",
            valor_gorjeta=valor_gorjeta,
            total=total,
            por_pessoa=por_pessoa,
            classificacao=classificacao,
            cor=cor
        )

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)