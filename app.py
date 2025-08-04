# Imports necessários
import streamlit as st
import datetime
import re
from collections import Counter

# --- Configurações Iniciais e Funções Auxiliares ---

pythagorean_map = {
    'A': 1, 'J': 1, 'S': 1, 'B': 2, 'K': 2, 'T': 2, 'C': 3, 'L': 3, 'U': 3,
    'D': 4, 'M': 4, 'V': 4, 'E': 5, 'N': 5, 'W': 5, 'F': 6, 'O': 6, 'X': 6,
    'G': 7, 'P': 7, 'Y': 7, 'H': 8, 'Q': 8, 'Z': 8, 'I': 9, 'R': 9
}
vowels = 'AEIOU'
karmic_debt_numbers = {13, 14, 16, 19}

def reduce_number(n, preserve_masters=True):
    """Reduz um número a um dígito. 
    Se preserve_masters=True, preserva números mestres 11 e 22 (padrão).
    Se preserve_masters=False, reduz TUDO a um dígito."""
    try:
        n = int(n)
    except (ValueError, TypeError):
        return 0
    is_negative = n < 0
    if is_negative:
        n = abs(n)
    
    if preserve_masters:
        while n > 9 and n not in [11, 22]:
            try:
                n = sum(int(digit) for digit in str(n))
            except ValueError:
                return 0
    else:
        while n > 9:
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

def calculate_personal_year(birth_day, birth_month, current_date):
    """Calcula o ano pessoal considerando se já fez aniversário."""
    current_year = current_date.year
    birthday_this_year = datetime.date(current_year, birth_month, birth_day)
    
    # Se ainda não fez aniversário este ano, usa o ano anterior
    if current_date < birthday_this_year:
        year_to_use = current_year - 1
    else:
        year_to_use = current_year
    
    reduced_day = reduce_number(birth_day, preserve_masters=False)
    reduced_month = reduce_number(birth_month, preserve_masters=False)
    reduced_year = reduce_number(year_to_use, preserve_masters=False)
    
    personal_year_sum = reduced_day + reduced_month + reduced_year
    return reduce_number(personal_year_sum, preserve_masters=True), year_to_use

def calculate_pinnacles(birth_date, life_path):
    """Calcula os 4 Pináculos da vida com idades específicas."""
    day = reduce_number(birth_date.day, preserve_masters=False)
    month = reduce_number(birth_date.month, preserve_masters=False)
    year = reduce_number(birth_date.year, preserve_masters=False)
    
    # Cálculo dos Pináculos (preserva números mestres no resultado)
    pinnacle1 = reduce_number(day + month)
    pinnacle2 = reduce_number(day + year)
    pinnacle3 = reduce_number(pinnacle1 + pinnacle2)
    pinnacle4 = reduce_number(month + year)
    
    # Cálculo das idades de transição (baseado no Caminho de Vida)
    first_pinnacle_end = 36 - life_path
    second_pinnacle_end = first_pinnacle_end + 9
    third_pinnacle_end = second_pinnacle_end + 9
    
    return {
        'pinnacle1': {'number': pinnacle1, 'age_start': 0, 'age_end': first_pinnacle_end},
        'pinnacle2': {'number': pinnacle2, 'age_start': first_pinnacle_end + 1, 'age_end': second_pinnacle_end},
        'pinnacle3': {'number': pinnacle3, 'age_start': second_pinnacle_end + 1, 'age_end': third_pinnacle_end},
        'pinnacle4': {'number': pinnacle4, 'age_start': third_pinnacle_end + 1, 'age_end': None},
        'ages': {
            'first': f"0 até {first_pinnacle_end} anos",
            'second': f"{first_pinnacle_end + 1} até {second_pinnacle_end} anos",
            'third': f"{second_pinnacle_end + 1} até {third_pinnacle_end} anos",
            'fourth': f"{third_pinnacle_end + 1} anos em diante"
        }
    }

def calculate_life_cycles(birth_date, life_path):
    """Calcula os 3 Ciclos de Vida com idades específicas."""
    month = reduce_number(birth_date.month, preserve_masters=False)
    day = reduce_number(birth_date.day, preserve_masters=False)
    year = reduce_number(birth_date.year, preserve_masters=False)
    
    # Os ciclos são baseados no mês, dia e ano
    cycle1 = month  # Ciclo Formativo
    cycle2 = day    # Ciclo Produtivo  
    cycle3 = year   # Ciclo de Colheita
    
    # Idades dos ciclos (baseadas no Caminho de Vida)
    # Método tradicional: primeiro ciclo termina em 27-Caminho de Vida
    first_cycle_end = 27 + (9 - life_path)
    if first_cycle_end < 27:
        first_cycle_end = 27
    second_cycle_end = first_cycle_end + 27
    
    return {
        'formative': {
            'number': cycle1, 
            'age_start': 0,
            'age_end': first_cycle_end,
            'period': f'0 até {first_cycle_end} anos'
        },
        'productive': {
            'number': cycle2,
            'age_start': first_cycle_end + 1,
            'age_end': second_cycle_end,
            'period': f'{first_cycle_end + 1} até {second_cycle_end} anos'
        },
        'harvest': {
            'number': cycle3,
            'age_start': second_cycle_end + 1,
            'age_end': None,
            'period': f'{second_cycle_end + 1} anos em diante'
        }
    }

def calculate_challenges(birth_date, life_path):
    """Calcula os Desafios com períodos baseados nos Pináculos."""
    day = reduce_number(birth_date.day, preserve_masters=False)
    month = reduce_number(birth_date.month, preserve_masters=False)
    year = reduce_number(birth_date.year, preserve_masters=False)
    
    # Cálculo dos desafios (sempre reduz tudo)
    challenge1 = abs(day - month)
    challenge1 = reduce_number(challenge1, preserve_masters=False)
    
    challenge2 = abs(day - year)
    challenge2 = reduce_number(challenge2, preserve_masters=False)
    
    challenge3 = abs(challenge1 - challenge2)
    challenge3 = reduce_number(challenge3, preserve_masters=False)
    
    challenge4 = abs(month - year)
    challenge4 = reduce_number(challenge4, preserve_masters=False)
    
    # As idades dos desafios seguem os pináculos
    first_pinnacle_end = 36 - life_path
    second_pinnacle_end = first_pinnacle_end + 9
    third_pinnacle_end = second_pinnacle_end + 9
    
    return {
        'challenge1': {
            'number': challenge1,
            'period': f"0 até {first_pinnacle_end} anos",
            'description': 'Desafio do 1º Pináculo'
        },
        'challenge2': {
            'number': challenge2,
            'period': f"{first_pinnacle_end + 1} até {second_pinnacle_end} anos",
            'description': 'Desafio do 2º Pináculo'
        },
        'challenge3': {
            'number': challenge3,
            'period': f"{second_pinnacle_end + 1} até {third_pinnacle_end} anos",
            'description': 'Desafio do 3º Pináculo'
        },
        'challenge4': {
            'number': challenge4,
            'period': f"{third_pinnacle_end + 1} anos em diante",
            'description': 'Desafio do 4º Pináculo'
        },
        'major_challenge': {
            'number': challenge3,
            'description': 'Desafio Principal da Vida'
        }
    }

def calculate_bridge_numbers(life_path, expression, soul_urge, personality):
    """Calcula os Números de Ponte entre os números principais."""
    bridges = {}
    
    # Ponte entre Caminho de Vida e Expressão
    bridges['life_expression'] = abs(life_path - expression)
    
    # Ponte entre Alma e Personalidade
    bridges['soul_personality'] = abs(soul_urge - personality)
    
    # Ponte entre Caminho de Vida e Alma
    bridges['life_soul'] = abs(life_path - soul_urge)
    
    # Ponte entre Expressão e Personalidade
    bridges['expression_personality'] = abs(expression - personality)
    
    # Os números de ponte não são reduzidos (representam a distância)
    return bridges

# --- Função Principal de Cálculo COMPLETA ---

def calculate_numerology_st(full_name, birth_date):
    """Calcula o mapa numerológico completo. Recebe string e date object."""
    results = {}
    karmic_debts_log = []
    current_date = datetime.date.today()

    # 1. Validar e Processar Nome
    if not full_name or not isinstance(full_name, str):
        raise ValueError("Nome inválido ou não fornecido.")
    
    cleaned_name_for_split = re.sub(r"[^a-zA-ZÀ-ú' -]", "", full_name).strip()
    name_parts_raw = re.findall(r"[\w'-]+", cleaned_name_for_split)
    name_parts = [part for part in name_parts_raw if len(part.replace("-","").replace("'","")) <= 25 and len(part.replace("-","").replace("'","")) > 0]

    if not (1 <= len(name_parts) <= 8):
        raise ValueError(f"O nome '{cleaned_name_for_split}' parece inválido. Deve ter entre 1 e 8 partes (1 nome + até 7 sobrenomes), com até 25 letras cada.")
    
    for part in name_parts:
        clean_part = part.replace("-","").replace("'","")
        if not (1 <= len(clean_part) <= 25):
            raise ValueError(f"A parte do nome '{part}' tem comprimento inválido após limpeza ({len(clean_part)}).")

    full_name_cleaned = " ".join(name_parts)
    results['Nome Completo'] = full_name_cleaned
    results['Data de Nascimento'] = birth_date.strftime('%d/%m/%Y')

    # 2. Processar Data de Nascimento
    day = birth_date.day
    month = birth_date.month
    year = birth_date.year

    # 3. Cálculos Principais

    # Número de Expressão (Destino) - Por partes (SEMPRE reduz nas partes)
    expression_sum_raw = 0
    reduced_part_values_expr = []
    expression_parts_detail = []
    
    for part in name_parts:
        part_sum_raw = get_number_value(part, use_vowels=None)
        expression_sum_raw += part_sum_raw
        # SEMPRE reduz, inclusive números mestres nas partes
        reduced_value = reduce_number(part_sum_raw, preserve_masters=False)
        reduced_part_values_expr.append(reduced_value)
        expression_parts_detail.append(f"{part}: {part_sum_raw} → {reduced_value}")
    
    final_expression_sum = sum(reduced_part_values_expr)
    karmic_debt_expr = check_karmic_debt(expression_sum_raw, "Soma Bruta da Expressão")
    if karmic_debt_expr: karmic_debts_log.append(karmic_debt_expr.strip())
    karmic_debt_expr_final = check_karmic_debt(final_expression_sum, "Soma das Partes Reduzidas da Expressão")
    if karmic_debt_expr_final: karmic_debts_log.append(karmic_debt_expr_final.strip())
    
    # Só preserva números mestres no resultado FINAL
    results['Número de Expressão (Destino)'] = reduce_number(final_expression_sum, preserve_masters=True)
    results['_expressao_detalhes'] = expression_parts_detail

    # Número de Motivação (Alma) - Mesmo processo
    motivation_sum_raw = 0
    reduced_part_values_motiv = []
    
    for part in name_parts:
        part_sum_raw_vowel = get_number_value(part, use_vowels=True)
        motivation_sum_raw += part_sum_raw_vowel
        # SEMPRE reduz nas partes
        reduced_part_values_motiv.append(reduce_number(part_sum_raw_vowel, preserve_masters=False))
    
    final_motivation_sum = sum(reduced_part_values_motiv)
    karmic_debt_motiv = check_karmic_debt(motivation_sum_raw, "Soma Bruta da Motivação")
    if karmic_debt_motiv: karmic_debts_log.append(karmic_debt_motiv.strip())
    karmic_debt_motiv_final = check_karmic_debt(final_motivation_sum, "Soma das Partes Reduzidas da Motivação")
    if karmic_debt_motiv_final: karmic_debts_log.append(karmic_debt_motiv_final.strip())
    
    # Preserva mestres só no final
    results['Número de Motivação (Alma)'] = reduce_number(final_motivation_sum, preserve_masters=True)

    # Número de Impressão (Personalidade) - Mesmo processo
    impression_sum_raw = 0
    reduced_part_values_impr = []
    
    for part in name_parts:
        part_sum_raw_consonant = get_number_value(part, use_vowels=False)
        impression_sum_raw += part_sum_raw_consonant
        # SEMPRE reduz nas partes
        reduced_part_values_impr.append(reduce_number(part_sum_raw_consonant, preserve_masters=False))
    
    final_impression_sum = sum(reduced_part_values_impr)
    karmic_debt_impr = check_karmic_debt(impression_sum_raw, "Soma Bruta da Impressão")
    if karmic_debt_impr: karmic_debts_log.append(karmic_debt_impr.strip())
    karmic_debt_impr_final = check_karmic_debt(final_impression_sum, "Soma das Partes Reduzidas da Impressão")
    if karmic_debt_impr_final: karmic_debts_log.append(karmic_debt_impr_final.strip())
    
    # Preserva mestres só no final
    results['Número de Impressão (Personalidade)'] = reduce_number(final_impression_sum, preserve_masters=True)

    # Número do Caminho de Vida
    # Reduz dia, mês e ano sempre (sem preservar mestres nas partes)
    reduced_day = reduce_number(day, preserve_masters=False)
    reduced_month = reduce_number(month, preserve_masters=False)
    reduced_year = reduce_number(year, preserve_masters=False)
    
    life_path_sum_reduced_parts = reduced_day + reduced_month + reduced_year
    karmic_debt_day = check_karmic_debt(day, f"Dia de Nascimento ({day})")
    if karmic_debt_day: karmic_debts_log.append(karmic_debt_day.strip())
    karmic_debt_lp = check_karmic_debt(life_path_sum_reduced_parts, "Soma (Reduzida) do Caminho de Vida")
    if karmic_debt_lp: karmic_debts_log.append(karmic_debt_lp.strip())
    
    # Preserva mestres só no resultado final
    results['Número do Caminho de Vida'] = reduce_number(life_path_sum_reduced_parts, preserve_masters=True)

    # Dia de Nascimento Reduzido (preserva mestres neste caso específico)
    results['Dia de Nascimento Reduzido'] = reduce_number(day, preserve_masters=True)

    # Número da Maturidade
    lp_num = results.get('Número do Caminho de Vida', 0)
    exp_num = results.get('Número de Expressão (Destino)', 0)
    maturity_sum = (lp_num if isinstance(lp_num, int) else 0) + \
                   (exp_num if isinstance(exp_num, int) else 0)
    results['Número da Maturidade'] = reduce_number(maturity_sum, preserve_masters=True)

    # Número de Equilíbrio (Das iniciais)
    initials = [part[0] for part in name_parts if part and part[0].isalpha()]
    equilibrium_sum = 0
    if initials:
        initial_values = [pythagorean_map.get(initial.upper(), 0) for initial in initials]
        equilibrium_sum = sum(initial_values)
    results['Número de Equilíbrio (Iniciais)'] = reduce_number(equilibrium_sum, preserve_masters=True)

    # Ano Pessoal (Corrigido para considerar aniversário)
    personal_year, year_used = calculate_personal_year(day, month, current_date)
    results[f'Ano Pessoal'] = personal_year
    results['_ano_pessoal_info'] = f"Baseado no ano {year_used}"

    # Lições Cármicas (Números Faltantes no Nome)
    all_letters = "".join(filter(str.isalpha, full_name_cleaned.upper()))
    letter_values = [pythagorean_map.get(char, 0) for char in all_letters]
    value_counts = Counter(letter_values)
    lessons = [i for i in range(1, 10) if value_counts[i] == 0]
    results['Lições Cármicas (Números Faltantes no Nome)'] = lessons if lessons else "Nenhuma"

    # NOVOS CÁLCULOS ADICIONADOS
    life_path = results['Número do Caminho de Vida']
    
    # Pináculos (com idades baseadas no Caminho de Vida)
    pinnacles = calculate_pinnacles(birth_date, life_path)
    results['Pináculos'] = pinnacles
    
    # Ciclos de Vida (com idades baseadas no Caminho de Vida)
    life_cycles = calculate_life_cycles(birth_date, life_path)
    results['Ciclos de Vida'] = life_cycles
    
    # Desafios (com períodos baseados nos Pináculos)
    challenges = calculate_challenges(birth_date, life_path)
    results['Desafios'] = challenges
    
    # Números de Ponte
    bridges = calculate_bridge_numbers(
        results['Número do Caminho de Vida'],
        results['Número de Expressão (Destino)'],
        results['Número de Motivação (Alma)'],
        results['Número de Impressão (Personalidade)']
    )
    results['Números de Ponte'] = bridges

    # Planos de Expressão (contagem de números no nome)
    plane_counts = Counter(letter_values)
    mental_plane = plane_counts[1] + plane_counts[8]  # Números 1 e 8
    physical_plane = plane_counts[4] + plane_counts[5]  # Números 4 e 5
    emotional_plane = plane_counts[2] + plane_counts[3] + plane_counts[6]  # Números 2, 3 e 6
    intuitive_plane = plane_counts[7] + plane_counts[9]  # Números 7 e 9
    
    results['Planos de Expressão'] = {
        'Mental': mental_plane,
        'Físico': physical_plane,
        'Emocional': emotional_plane,
        'Intuitivo': intuitive_plane
    }

    # Retorna os resultados e a lista separada de dívidas cármicas
    return results, karmic_debts_log


# --- Interface Streamlit ---
st.set_page_config(page_title="Calculadora Numerológica Completa por Marcos Inoue", layout="wide")

st.title("Calculadora de Numerologia Pitagórica Completa 🔢")
st.caption("por Marcos Inoue - Versão Aprimorada")

st.markdown("""
Bem-vindo(a)! Insira o nome completo de nascimento (exatamente como no registro)
e a data de nascimento para calcular o mapa numerológico pitagórico completo.


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
    submitted = st.form_submit_button("✨ Calcular Mapa Completo ✨")

# --- Processamento e Exibição ---
if submitted:
    if not user_name:
        st.error("Por favor, insira o nome completo.")
    elif user_dob is None:
        st.error("Por favor, selecione a data de nascimento.")
    else:
        try:
            # --- Calcular ---
            with st.spinner('Calculando seu mapa numerológico completo...'):
                results, karmic_debts_log = calculate_numerology_st(user_name, user_dob)

            # --- Exibir Resultados ---
            st.success("🎉 Mapa Numerológico Completo Calculado! 🎉")
            st.markdown(f"**Nome Considerado:** {results['Nome Completo']}")
            st.markdown(f"**Data de Nascimento:** {results['Data de Nascimento']}")

            # Criar abas para melhor organização
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Números Principais", "🔄 Ciclos e Desafios", "🌉 Números de Ponte", "✨ Aspectos Cármicos", "📋 Resumo Completo"])
            
            with tab1:
                st.subheader("Núcleo do Mapa Numerológico")
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("🛤️ Caminho de Vida", results['Número do Caminho de Vida'])
                col2.metric("🌟 Expressão (Destino)", results['Número de Expressão (Destino)'])
                col3.metric("💖 Motivação (Alma)", results['Número de Motivação (Alma)'])
                col4.metric("🎭 Impressão (Personalidade)", results['Número de Impressão (Personalidade)'])
                
                # Mostrar detalhes do cálculo da Expressão
                with st.expander("Ver detalhes do cálculo da Expressão"):
                    st.write("**Cálculo por partes do nome:**")
                    for detail in results['_expressao_detalhes']:
                        st.write(f"• {detail}")
                
                st.divider()
                
                st.subheader("Outros Números Importantes")
                col_outros1, col_outros2, col_outros3, col_outros4 = st.columns(4)
                col_outros1.metric("☀️ Dia Nascimento", results['Dia de Nascimento Reduzido'])
                col_outros2.metric("🌱 Maturidade", results['Número da Maturidade'])
                col_outros3.metric("⚖️ Equilíbrio", results['Número de Equilíbrio (Iniciais)'])
                col_outros4.metric("📅 Ano Pessoal", results['Ano Pessoal'], help=results['_ano_pessoal_info'])
                
                st.divider()
                
                st.subheader("Planos de Expressão")
                col_plane1, col_plane2, col_plane3, col_plane4 = st.columns(4)
                planes = results['Planos de Expressão']
                col_plane1.metric("🧠 Mental", planes['Mental'])
                col_plane2.metric("💪 Físico", planes['Físico'])
                col_plane3.metric("❤️ Emocional", planes['Emocional'])
                col_plane4.metric("🔮 Intuitivo", planes['Intuitivo'])
            
            with tab2:
                st.subheader("🏔️ Pináculos da Vida")
                pinnacles = results['Pináculos']
                
                col_p1, col_p2, col_p3, col_p4 = st.columns(4)
                col_p1.metric(
                    "1º Pináculo", 
                    pinnacles['pinnacle1']['number'], 
                    f"{pinnacles['pinnacle1']['age_start']}-{pinnacles['pinnacle1']['age_end']} anos"
                )
                col_p2.metric(
                    "2º Pináculo", 
                    pinnacles['pinnacle2']['number'], 
                    f"{pinnacles['pinnacle2']['age_start']}-{pinnacles['pinnacle2']['age_end']} anos"
                )
                col_p3.metric(
                    "3º Pináculo", 
                    pinnacles['pinnacle3']['number'], 
                    f"{pinnacles['pinnacle3']['age_start']}-{pinnacles['pinnacle3']['age_end']} anos"
                )
                col_p4.metric(
                    "4º Pináculo", 
                    pinnacles['pinnacle4']['number'], 
                    f"{pinnacles['pinnacle4']['age_start']}+ anos"
                )
                
                st.divider()
                
                st.subheader("🔄 Ciclos de Vida")
                cycles = results['Ciclos de Vida']
                
                col_c1, col_c2, col_c3 = st.columns(3)
                col_c1.metric("Ciclo Formativo", cycles['formative']['number'], cycles['formative']['period'])
                col_c2.metric("Ciclo Produtivo", cycles['productive']['number'], cycles['productive']['period'])
                col_c3.metric("Ciclo de Colheita", cycles['harvest']['number'], cycles['harvest']['period'])
                
                st.divider()
                
                st.subheader("🧗 Desafios da Vida")
                challenges = results['Desafios']
                
                # Mostrar os 4 desafios com seus períodos
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    st.metric(
                        "1º Desafio", 
                        challenges['challenge1']['number'],
                        challenges['challenge1']['period']
                    )
                    st.metric(
                        "3º Desafio", 
                        challenges['challenge3']['number'],
                        challenges['challenge3']['period']
                    )
                
                with col_d2:
                    st.metric(
                        "2º Desafio", 
                        challenges['challenge2']['number'],
                        challenges['challenge2']['period']
                    )
                    st.metric(
                        "4º Desafio", 
                        challenges['challenge4']['number'],
                        challenges['challenge4']['period']
                    )
                
                # Desafio Principal
                st.info(f"**Desafio Principal da Vida:** {challenges['major_challenge']['number']} - Este é o desafio central que permeia toda a vida")
            
            with tab3:
                st.subheader("🌉 Números de Ponte")
                st.write("Os Números de Ponte indicam as diferenças entre seus números principais e sugerem áreas onde você pode trabalhar para maior integração pessoal.")
                
                bridges = results['Números de Ponte']
                
                col_b1, col_b2 = st.columns(2)
                with col_b1:
                    st.metric("Vida ↔ Expressão", bridges['life_expression'])
                    st.metric("Vida ↔ Alma", bridges['life_soul'])
                
                with col_b2:
                    st.metric("Alma ↔ Personalidade", bridges['soul_personality'])
                    st.metric("Expressão ↔ Personalidade", bridges['expression_personality'])
            
            with tab4:
                st.subheader("Aspectos Cármicos")
                
                # Lições Cármicas
                licoes = results['Lições Cármicas (Números Faltantes no Nome)']
                if licoes == "Nenhuma":
                    st.info("**Lições Cármicas:** Nenhuma - Você tem todos os números de 1 a 9 representados em seu nome!")
                else:
                    st.warning(f"**Lições Cármicas (Números Faltantes):** {', '.join(map(str, licoes))}")
                    st.write("Estes números representam qualidades que você precisa desenvolver nesta vida.")
                
                # Dívidas Cármicas
                if not karmic_debts_log:
                    st.info("**Dívidas Cármicas:** Nenhuma detectada nos cálculos principais.")
                else:
                    st.warning("**Dívidas Cármicas Detectadas:**")
                    for debt in karmic_debts_log:
                        st.markdown(f"• {debt}")
            
            with tab5:
                st.subheader("📋 Resumo Completo do Mapa")
                
                # Criar duas colunas para o resumo
                col_summary1, col_summary2 = st.columns(2)
                
                with col_summary1:
                    st.markdown("### Números Principais")
                    st.write(f"**Caminho de Vida:** {results['Número do Caminho de Vida']}")
                    st.write(f"**Expressão/Destino:** {results['Número de Expressão (Destino)']}")
                    st.write(f"**Motivação/Alma:** {results['Número de Motivação (Alma)']}")
                    st.write(f"**Impressão/Personalidade:** {results['Número de Impressão (Personalidade)']}")
                    st.write(f"**Dia de Nascimento:** {results['Dia de Nascimento Reduzido']}")
                    st.write(f"**Maturidade:** {results['Número da Maturidade']}")
                    st.write(f"**Equilíbrio:** {results['Número de Equilíbrio (Iniciais)']}")
                    st.write(f"**Ano Pessoal:** {results['Ano Pessoal']} ({results['_ano_pessoal_info']})")
                
                with col_summary2:
                    st.markdown("### Ciclos e Desafios")
                    st.write(f"**Pináculos:** {pinnacles['pinnacle1']['number']}, {pinnacles['pinnacle2']['number']}, {pinnacles['pinnacle3']['number']}, {pinnacles['pinnacle4']['number']}")
                    st.write(f"**Ciclos:** {cycles['formative']['number']}, {cycles['productive']['number']}, {cycles['harvest']['number']}")
                    
                    challenges_numbers = f"{challenges['challenge1']['number']}, {challenges['challenge2']['number']}, {challenges['challenge3']['number']}, {challenges['challenge4']['number']}"
                    st.write(f"**Desafios:** {challenges_numbers}")
                    st.write(f"**Desafio Principal:** {challenges['major_challenge']['number']}")
                    
                    # Aspectos Cármicos no resumo
                    if licoes != "Nenhuma":
                        st.write(f"**Lições Cármicas:** {', '.join(map(str, licoes))}")
                    else:
                        st.write("**Lições Cármicas:** Nenhuma")
                    
                    if karmic_debts_log:
                        st.write(f"**Dívidas Cármicas:** {len(karmic_debts_log)} encontrada(s)")

        except ValueError as e:
            st.error(f"⚠️ Erro nos dados inseridos: {e}")
        except Exception as e:
            st.error(f"❌ Ocorreu um erro inesperado durante o cálculo.")
            st.exception(e)

# --- Rodapé ---
st.divider()
st.caption("""
**Calculadora baseada na numerologia Pitagórica.**
- Método de cálculo por partes do nome para maior precisão
- Ano Pessoal considera se já fez aniversário no ano atual
- Números mestres: 11 e 22 (não usa 33)
- A interpretação dos números requer estudo aprofundado
""")

# --- Informações Adicionais ---
with st.expander("ℹ️ Sobre os Cálculos"):
    st.markdown("""
    ### Método de Cálculo da Expressão
    Este programa usa o método de **cálculo por partes**, que é mais preciso:
    1. Calcula o valor numérico de cada parte do nome separadamente
    2. Reduz cada parte individualmente
    3. Soma os valores reduzidos
    4. Reduz o resultado final
    
    Este método permite identificar melhor números mestres (11, 22) em nomes compostos.
    
    ### Exemplo: Marcos Antonio Inoue Rosa
    - MARCOS: M(4)+A(1)+R(9)+C(3)+O(6)+S(1) = 24 → 6
    - ANTONIO: A(1)+N(5)+T(2)+O(6)+N(5)+I(9)+O(6) = 34 → 7
    - INOUE: I(9)+N(5)+O(6)+U(3)+E(5) = 28 → 1
    - ROSA: R(9)+O(6)+S(1)+A(1) = 17 → 8
    - Soma: 6 + 7 + 1 + 8 = 22 (número mestre preservado!)
    
    **Importante:** Se somássemos todas as letras diretamente (24+34+28+17 = 103 → 4), perderíamos o número mestre 22!
    
    ### Ano Pessoal
    O cálculo considera se você já fez aniversário no ano atual:
    - Se já fez aniversário: usa o ano atual
    - Se ainda não fez: usa o ano anterior
    """)

