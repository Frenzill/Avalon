import random
import math

# Функция для генерации списка ролей
def generate_roles(num_players):
    if num_players < 5 or num_players > 10:
        print("Количество игроков должно быть от 5 до 10.")
        return None
    
    spy_count = math.floor((num_players - 1) / 3) + 1
    resistance_count = num_players - spy_count
    
    roles = ['Шпион'] * spy_count + ['Сопротивление'] * resistance_count
    random.shuffle(roles)
    
    return roles

def assign_roles(num_players):
    roles = generate_roles(num_players)
    if roles is None:
        return
    
    players = [f"Игрок {i}" for i in range(1, num_players + 1)]
    player_roles = dict(zip(players, roles))
    
    leader, hammer = get_leader_and_hammer(players)
    
    print("Роли для игроков:")
    for player, role in player_roles.items():
        print(f"{player}: {role}")
    
    print(f"Лидер: {leader}")
    print(f"Хаммер: {hammer}")
    
    while True:
        active_player = input("Введите имя активного игрока: ")
        if active_player not in player_roles:
            print("Неверное имя игрока.")
            continue
        
        if active_player == leader:
            print("Вы лидер. Выберите игрока для миссии.")
            mission_player = input("Введите имя игрока для миссии: ")
            if mission_player not in player_roles:
                print("Неверное имя игрока.")
                continue
            
            print(f"Вы выбрали игрока {mission_player} для миссии.")
            
            # Голосование за или против команды
            votes = conduct_voting(players)
            
            # Подсчет результатов голосования
            vote_count = len(votes)
            votes_for = sum(votes.values())
            votes_against = vote_count - votes_for
            
            if votes_for > votes_against:
                print("Команда одобрена. Миссия начинается...")
                mission_success = conduct_mission(mission_player, player_roles)
                
                if mission_success:
                    print("Миссия успешно выполнена!")
                else:
                    print("Миссия провалена!")
                
            else:
                print("Команда отклонена.")
                if active_player == hammer:
                    print("Шпионы выиграли!")
                else:
                    leader, hammer = transfer_leadership(players, leader, hammer)
                    print(f"Лидерство передано игроку {leader}")
        
        else:
            print(f"Ваша роль: {player_roles[active_player]}")
        
        break

# Функция для проведения голосования
def conduct_voting(players):
    votes = {}
    for player in players:
        vote = input(f"{player}, вы голосуете 'за' или 'против'? ")
        if vote.lower() == 'за':
            votes[player] = 1
        else:
            votes[player] = 0
    return votes

# Функция для проведения миссии
def conduct_mission(mission_player, player_roles):
    mission_role = player_roles[mission_player]
    
    if mission_role == 'Сопротивление':
        print(f"Игрок {mission_player} выполняет миссию...")
        return True
    elif mission_role == 'Шпион':
        decision = input(f"Игрок {mission_player}, успешно пройти миссию? (Да/Нет) ")
        if decision.lower() == 'да':
            print(f"Игрок {mission_player} успешно провел миссию.")
            return True
        else:
            print(f"Игрок {mission_player} провалил миссию.")
            return False

# Функция для передачи роли лидера следующему игроку
def transfer_leadership(players, leader, hammer):
    leader_index = players.index(leader)
    next_leader_index = (leader_index + 1) % len(players)
    next_leader = players[next_leader_index]
    
    print(f"Лидерство передано игроку {next_leader}")
    return next_leader, hammer

# Функция для выдачи Лидера и Хаммера
def get_leader_and_hammer(players):
    leader = random.choice(players)
    hammer_index = (players.index(leader) + 4) % len(players)
    hammer = players[hammer_index]
    return leader, hammer

# Пример использования
num_players = int(input("Введите количество игроков (от 5 до 10): "))
assign_roles(num_players)
