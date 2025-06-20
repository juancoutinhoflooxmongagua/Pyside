PRIMARY_COLOR = "#3498db"
DARKER_PRIMARY_COLOR = "#2980b9"
DARKEST_PRIMARY_COLOR = "#2471a3"

qss = f"""
    /*
     * Estilo para o nosso botão especial, identificado pela
     * propriedade dinâmica 'class' com o valor 'specialButton'.
     */
    QPushButton[class="specialButton"] {{
        color: white;
        background-color: {PRIMARY_COLOR};
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
    }}

    /* Efeito ao passar o mouse por cima */
    QPushButton[class="specialButton"]:hover {{
        background-color: {DARKER_PRIMARY_COLOR};
    }}

    /* Efeito ao pressionar o botão */
    QPushButton[class="specialButton"]:pressed {{
        background-color: {DARKEST_PRIMARY_COLOR};
    }}
"""
