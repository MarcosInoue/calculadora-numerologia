# Imports necessários
import streamlit as st
import datetime
import re
from collections import Counter

# --- Configurações Iniciais e Funções Auxiliares ---
# (Exatamente as mesmas funções de antes: pythagorean_map, vowels, karmic_debt_numbers,
#  reduce_number, get_number_value, check_karmic_debt)

pythagorean_map = {
    'A': 1, 'J': 1, 'S': 1, 'B': 2, 'K': 2, 'T': 2, 'C': 3, 'L': 3, 'U': 3,
    'D': 4, 'M': 4, 'V': 4, 'E': 5, 'N': 5, 'W': 5, 'F': 6, 'O': 6, 'X': 6,
    'G': 7, 'P': 7, 'Y': 7, 'H': 8, 'Q': 8, 'Z': 8, 'I': 9, 'R': 9
}
vowels = 'AEIOU'
karmic_debt_numbers = {13, 14, 16, 19}

def reduce_number(n):
    """Reduz um número a um dígito ou número mestre (11, 22)."""
    try:
        n = int(n)
    except (ValueError, TypeError):
        return 0
    is_negative = n < 0
    if is_negative:
        n = abs(n)
    while n > 9 and n not in [11, 22]:
        try:
            n = sum(int(digit) for digit in str(n))
        except ValueError:
            return 0
    return n

def get_number_value(text, use_vowels=None):
    """Calcula a soma numérica bruta de um texto (nome/sobrenome)."""
    value = 0
    if not isinstance(text, str):
        return 0
    for char in text.upper():
        if char.isalpha():
            is_vowel = char in vowels
            if use_vowels is True and is_vowel:
                value += pythagorean_map.get(char, 0)
            elif use_vowels is False and not is_vowel:
                 value += pythagorean_map.get(char, 0)
            elif use_vowels is None:
                 value += pythagorean_map.get(char, 0)
    return value

def check_karmic_debt(number, calculation_name):
    """Verifica e retorna a string de dívida cármica se aplicável."""
    if number in karmic_debt_numbers:
        return f" (Dívida Cármica {number} encontrada em {calculation_name})"
    return ""

# --- Função Principal de Cálculo (Adaptada para Streamlit) ---
# (Exatamente a mesma função de antes: calculate_numerology_st)

def calculate_numerology_st(full_name, birth_date):
    """Calcula o mapa numerológico completo. Recebe string e date object."""
    results = {}
    karmic_debts_log = []

    # 1. Validar e Processar Nome
    if not full_name or not isinstance(full_name, str):
         raise ValueError("Nome inválido ou não fornecido.")
    cleaned_name_for_split = re.sub(r"[^a-zA-ZÀ-ú' -]", "", full_name).strip()
    name_parts_raw = re.findall(r"[\w'-]+", cleaned_name_for_split)
    name_parts = [part for part in name_parts_raw if len(part.replace("-","").replace("'","")) <= 15 and len(part.replace("-","").replace("'","")) > 0]

    if not (1 <= len(name_parts) <= 6):
        raise ValueError(f"O nome '{cleaned_name_for_split}' parece inválido. Deve ter entre 1 e 6 partes (1 nome + até 5 sobrenomes), com até 15 letras cada.")
    for part in name_parts:
         clean_part = part.replace("-","").replace("'","")
         if not (1 <= len(clean_part) <= 15):
              raise ValueError(f"A parte do nome '{part}' tem comprimento inválido após limpeza ({len(clean_part)}).")

    full_name_cleaned = " ".join(name_parts)
    results['Nome Completo'] = full_name_cleaned
    results['Data de Nascimento'] = birth_date.strftime('%d/%m/%Y')

    # 2. Processar Data de Nascimento
    day = birth_date.day
    month = birth_date.month
    year = birth_date.year
    reduced_day = reduce_number(day)
    reduced_month = reduce_number(month)
    reduced_year = reduce_number(year)

    # 3. Cálculos Principais (Expressão, Motivação, Impressão, Caminho Vida, etc...)
    # (Lógica interna exatamente igual à anterior)

    # Número de Expressão (Destino)
    expression_sum_raw = 0
    reduced_part_values_expr = []
    for part in name_parts:
        part_sum_raw = get_number_value(part, use_vowels=None)
        expression_sum_raw += part_sum_raw
        reduced_part_values_expr.append(reduce_number(part_sum_raw))
    final_expression_sum = sum(reduced_part_values_expr)
    karmic_debt_expr = check_karmic_debt(expression_sum_raw, "Soma Bruta da Expressão")
    if karmic_debt_expr: karmic_debts_log.append(karmic_debt_expr.strip())
    karmic_debt_expr_final = check_karmic_debt(final_expression_sum, "Soma das Partes Reduzidas da Expressão")
    if karmic_debt_expr_final: karmic_debts_log.append(karmic_debt_expr_final.strip())
    results['Número de Expressão (Destino)'] = reduce_number(final_expression_sum)

    # Número de Motivação (Alma / Desejo de Alma)
    motivation_sum_raw = 0
    reduced_part_values_motiv = []
    for part in name_parts:
        part_sum_raw_vowel = get_number_value(part, use_vowels=True)
        motivation_sum_raw += part_sum_raw_vowel
        reduced_part_values_motiv.append(reduce_number(part_sum_raw_vowel))
    final_motivation_sum = sum(reduced_part_values_motiv)
    karmic_debt_motiv = check_karmic_debt(motivation_sum_raw, "Soma Bruta da Motivação")
    if karmic_debt_motiv: karmic_debts_log.append(karmic_debt_motiv.strip())
    karmic_debt_motiv_final = check_karmic_debt(final_motivation_sum, "Soma das Partes Reduzidas da Motivação")
    if karmic_debt_motiv_final: karmic_debts_log.append(karmic_debt_motiv_final.strip())
    results['Número de Motivação (Alma)'] = reduce_number(final_motivation_sum)
    results['Número do Desejo de Alma'] = results['Número de Motivação (Alma)']

    # Número de Impressão (Personalidade / Sonho)
    impression_sum_raw = 0
    reduced_part_values_impr = []
    for part in name_parts:
        part_sum_raw_consonant = get_number_value(part, use_vowels=False)
        impression_sum_raw += part_sum_raw_consonant
        reduced_part_values_impr.append(reduce_number(part_sum_raw_consonant))
    final_impression_sum = sum(reduced_part_values_impr)
    karmic_debt_impr = check_karmic_debt(impression_sum_raw, "Soma Bruta da Impressão")
    if karmic_debt_impr: karmic_debts_log.append(karmic_debt_impr.strip())
    karmic_debt_impr_final = check_karmic_debt(final_impression_sum, "Soma das Partes Reduzidas da Impressão")
    if karmic_debt_impr_final: karmic_debts_log.append(karmic_debt_impr_final.strip())
    results['Número de Impressão (Personalidade)'] = reduce_number(final_impression_sum)

    # Número do Caminho de Vida
    life_path_sum_reduced_parts = reduced_day + reduced_month + reduced_year
    karmic_debt_day = check_karmic_debt(day, f"Dia de Nascimento ({day})")
    if karmic_debt_day: karmic_debts_log.append(karmic_debt_day.strip())
    karmic_debt_lp = check_karmic_debt(life_path_sum_reduced_parts, "Soma (Reduzida) do Caminho de Vida")
    if karmic_debt_lp: karmic_debts_log.append(karmic_debt_lp.strip())
    results['Número do Caminho de Vida'] = reduce_number(life_path_sum_reduced_parts)
    results['Número de Propósito'] = f"Geralmente associado ao Caminho de Vida ({results['Número do Caminho de Vida']})"

    # Dia de Nascimento Reduzido
    results['Dia de Nascimento Reduzido'] = reduced_day

    # Número da Maturidade
    lp_num = results.get('Número do Caminho de Vida', 0)
    exp_num = results.get('Número de Expressão (Destino)', 0)
    maturity_sum = (lp_num if isinstance(lp_num, int) else 0) + \
                   (exp_num if isinstance(exp_num, int) else 0)
    results['Número da Maturidade'] = reduce_number(maturity_sum)

    # Número de Equilíbrio (Das iniciais)
    initials = [part[0] for part in name_parts if part and part[0].isalpha()]
    equilibrium_sum = 0
    if initials:
         initial_values = [pythagorean_map.get(initial.upper(), 0) for initial in initials]
         equilibrium_sum = sum(initial_values)
    results['Número de Equilíbrio (Iniciais)'] = reduce_number(equilibrium_sum)

    # Ano Pessoal
    current_year = datetime.date.today().year
    reduced_current_year = reduce_number(current_year)
    personal_year_sum = reduced_day + reduced_month + reduced_current_year
    results[f'Ano Pessoal ({current_year})'] = reduce_number(personal_year_sum)

    # Desafios
    challenge1 = abs(reduced_day - reduced_month)
    results['Desafio 1 (Dia-Mês)'] = reduce_number(challenge1) if challenge1 not in [11,22] else reduce_number(sum(int(d) for d in str(challenge1)))
    challenge2 = abs(reduced_month - reduced_year)
    results['Desafio 2 (Mês-Ano)'] = reduce_number(challenge2) if challenge2 not in [11,22] else reduce_number(sum(int(d) for d in str(challenge2)))
    major_challenge = abs(results['Desafio 1 (Dia-Mês)'] - results['Desafio 2 (Mês-Ano)'])
    results['Desafio Maior (Desafio1-Desafio2)'] = reduce_number(major_challenge) if major_challenge not in [11,22] else reduce_number(sum(int(d) for d in str(major_challenge)))

    # Lições Cármicas (Números Faltantes no Nome)
    all_letters = "".join(filter(str.isalpha, full_name_cleaned.upper()))
    letter_values = [pythagorean_map.get(char, 0) for char in all_letters]
    value_counts = Counter(letter_values)
    lessons = [i for i in range(1, 10) if value_counts[i] == 0]
    results['Lições Cármicas (Números Faltantes no Nome)'] = lessons if lessons else "Nenhuma"

    # ---- APAGUE OU COMENTE ESTA LINHA ABAIXO ----
# results['Número da Saúde'] = ("Não há um cálculo único padrão. Analise o Caminho de Vida, Desafios, Lições, Expressão, etc., em conjunto.")
# ---- FIM DA LINHA A SER REMOVIDA/COMENTADA ----

    # Retorna os resultados e a lista separada de dívidas cármicas
    return results, karmic_debts_log


# --- Interface Streamlit ---
# ***** ALTERAÇÃO AQUI: Atualiza o título da aba do navegador *****
st.set_page_config(page_title="Calculadora Numerológica por Marcos Inoue", layout="centered")

st.title("Calculadora de Numerologia Pitagórica 🔢")
# ***** ALTERAÇÃO AQUI: Adiciona a linha de crédito *****
st.caption("por Marcos Inoue")

st.markdown("""
Bem-vindo(a)! Insira o nome completo de nascimento (exatamente como no registro)
e a data de nascimento para calcular o mapa numerológico pitagórico.
""")

# --- Inputs do Usuário ---
with st.form("numerology_form"):
    user_name = st.text_input("**Nome Completo de Nascimento:**", placeholder="Ex: Maria Joaquina de Amaral Pereira Góis")
    user_dob = st.date_input(
        "**Data de Nascimento:**",
        value=None,
        min_value=datetime.date(1900, 1, 1),
        max_value=datetime.date.today(),
        format="DD/MM/YYYY"
    )
    submitted = st.form_submit_button("✨ Calcular Mapa ✨")

# --- Processamento e Exibição ---
if submitted:
    if not user_name:
        st.error("Por favor, insira o nome completo.")
    elif user_dob is None:
         st.error("Por favor, selecione a data de nascimento.")
    else:
        try:
            # --- Calcular ---
            with st.spinner('Calculando seu mapa...'):
                # Chama a função de cálculo que retorna resultados e dívidas
                results, karmic_debts_log = calculate_numerology_st(user_name, user_dob)

            # --- Exibir Resultados ---
            st.success("🎉 Mapa Numerológico Calculado! 🎉")
            st.markdown(f"**Nome Considerado:** {results['Nome Completo']}")
            st.markdown(f"**Data de Nascimento:** {results['Data de Nascimento']}")

            st.divider()

            st.subheader("Núcleo do Mapa:")
            col1, col2 = st.columns(2) # Usando 2 colunas para melhor encaixe
            col1.metric("💖 Motivação (Alma)", results['Número de Motivação (Alma)'])
            col2.metric("🎭 Impressão (Personalidade)", results['Número de Impressão (Personalidade)'])

            # Colocando Caminho de Vida e Expressão abaixo para mais espaço
            st.metric("🛤️ Caminho de Vida", results['Número do Caminho de Vida'])
            st.metric("🌟 Expressão (Destino)", results['Número de Expressão (Destino)'])

            st.divider()

            st.subheader("Outros Números Importantes:")
            col_outros1, col_outros2, col_outros3 = st.columns(3)
            col_outros1.metric("☀️ Dia Nascimento Red.", results['Dia de Nascimento Reduzido'])
            col_outros2.metric("🌱 Maturidade", results['Número da Maturidade'])
            col_outros3.metric("⚖️ Equilíbrio (Iniciais)", results['Número de Equilíbrio (Iniciais)'])

            # Ano Pessoal - Usa o ano atual dinamicamente
            current_year_for_display = datetime.date.today().year
            st.metric(f"📅 Ano Pessoal ({current_year_for_display})", results[f'Ano Pessoal ({current_year_for_display})'])

            st.divider()

            st.subheader("Desafios:")
            col_desafio1, col_desafio2, col_desafio3 = st.columns(3)
            col_desafio1.metric("🧗 Desafio 1 (Dia-Mês)", results['Desafio 1 (Dia-Mês)'])
            col_desafio2.metric("🧗 Desafio 2 (Mês-Ano)", results['Desafio 2 (Mês-Ano)'])
            col_desafio3.metric("🏆 Desafio Maior", results['Desafio Maior (Desafio1-Desafio2)'])

            st.divider()

            st.subheader("Aspectos Cármicos:")
            # Lições Cármicas
            licoes = results['Lições Cármicas (Números Faltantes no Nome)']
            if licoes == "Nenhuma":
                st.write("**Lições Cármicas (Números Faltantes):** Nenhuma")
            else:
                st.write(f"**Lições Cármicas (Números Faltantes):** {', '.join(map(str, licoes))}")

            # Dívidas Cármicas (usa a lista retornada pela função)
            if not karmic_debts_log:
                st.write("**Dívidas Cármicas:** Nenhuma detectada nos cálculos principais.")
            else:
                st.warning("**Dívidas Cármicas Detectadas:**")
                for debt in karmic_debts_log:
                    st.markdown(f"* {debt}") # Usa markdown para formatar como lista

            st.divider()
            st.info(f"**Nota sobre Saúde:** {results['Número da Saúde']}")

        except ValueError as e:
            st.error(f"⚠️ Erro nos dados inseridos: {e}")
        except Exception as e:
            st.error(f"❌ Ocorreu um erro inesperado durante o cálculo.")
            # Para depuração, você pode descomentar a linha abaixo para ver o erro completo no app
            st.exception(e)

# --- Rodapé (Opcional) ---
st.divider()
st.caption("Calculadora baseada na numerologia Pitagórica. A interpretação dos números requer estudo.")
# Você pode adicionar seu nome aqui no rodapé também, se quiser.
# st.caption("Desenvolvido por Marcos Inoue.")