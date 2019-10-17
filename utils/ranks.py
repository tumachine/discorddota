ranks = {0: 'Herald', 1: 'Guardian', 2: 'Crusader', 3: 'Archon', 4: 'Legend', 5: 'Ancient', 6: 'Divine'}


def get_rank_from_dict_history(stratz_ranks):
    previous_rank = 1
    rank = 1
    for stratz_rank in stratz_ranks:
        if stratz_rank['seasonId'] == 2:
            previous_rank = stratz_rank['rank']
        elif stratz_rank['seasonId'] == 3:
            rank = stratz_rank['rank']
    return rank, previous_rank


def parse_rank_id(rank: int):
    if rank < 10:
        return 'Unknown'

    if rank == 80:
        return 'Immortal'

    rank_name = ranks[(rank // 10) - 1]
    rank_number = (rank % 10) // 2 + 1
    return f'{rank_name} {rank_number}'
