from datetime import datetime, timedelta


DIAS_SEMANA = {
    "Segunda": 0,
    "Terça": 1,
    "Quarta": 2,
    "Quinta": 3,
    "Sexta": 4,
    "Sábado": 5,
    "Domingo": 6,
}


def obter_proxima_aula(materia):
    agora = datetime.now()

    melhor_aula = None

    for horario in materia.horarios.all():

        dia = DIAS_SEMANA.get(horario.dia)

        if dia is None:
            continue

        diferenca_dias = (dia - agora.weekday()) % 7

        data_aula = agora.date() + timedelta(
            days=diferenca_dias
        )

        inicio = datetime.combine(
            data_aula,
            horario.hora_inicio
        )

        # Se for hoje, mas a aula já passou,
        # procuramos a próxima ocorrência semanal.
        if inicio <= agora:
            data_aula += timedelta(days=7)

            inicio = datetime.combine(
                data_aula,
                horario.hora_inicio
            )

        if melhor_aula is None or inicio < melhor_aula:
            melhor_aula = inicio

    return melhor_aula