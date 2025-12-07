import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from typing import List, Dict, Any

def load_users_data() -> List[Dict[str, Any]]:
    try:
        users_tree = ET.parse('users.xml')
        users = []
        for user_elem in users_tree.getroot().findall('user'):
            user = {
                'user_id': int(user_elem.find('user_id').text),
                'name': user_elem.find('name').text,
                'age': int(user_elem.find('age').text),
                'weight': int(user_elem.find('weight').text),
                'fitness_level': user_elem.find('fitness_level').text,
                'workouts': []
            }
            users.append(user)
        return users
    except FileNotFoundError:
        print("Файл users.xml не найден")
        return []

def load_workouts_data() -> List[Dict[str, Any]]:
    try:
        workouts_tree = ET.parse('workouts.xml')
        workouts = []
        for workout_elem in workouts_tree.getroot().findall('workout'):
            workout = {
                'workout_id': int(workout_elem.find('workout_id').text),
                'user_id': int(workout_elem.find('user_id').text),
                'date': workout_elem.find('date').text,
                'type': workout_elem.find('type').text,
                'duration': int(workout_elem.find('duration').text),
                'distance': float(workout_elem.find('distance').text),
                'calories': int(workout_elem.find('calories').text),
                'avg_heart_rate': int(workout_elem.find('avg_heart_rate').text),
                'intensity': workout_elem.find('intensity').text
            }
            workouts.append(workout)
        return workouts
    except FileNotFoundError:
        print("Файл workouts.xml не найден")
        return []

def get_stats(users: List[Dict[str, Any]], workouts: List[Dict[str, Any]]) -> None:
    total_workouts = len(workouts)
    total_users = len(users)
    total_calories = sum(w['calories'] for w in workouts)
    total_time_hours = sum(w['duration'] for w in workouts) / 60.0
    total_distance = sum(w['distance'] for w in workouts)

    print("ОБЩАЯ СТАТИСТИКА")
    print("=" * 50)
    print(f"Всего тренировок: {total_workouts}")
    print(f"Всего пользователей: {total_users}")
    print(f"Сожжено калорий: {total_calories}")
    print(f"Общее время: {total_time_hours:.1f} часов")
    print(f"Пройдено дистанции: {total_distance:.1f} км")
    print()

def analyze_user_activity(users: List[Dict[str, Any]], workouts: List[Dict[str, Any]]) -> None:
    for user in users:
        user_workouts = [w for w in workouts if w['user_id'] == user['user_id']]
        user['total_workouts'] = len(user_workouts)
        user['total_calories'] = sum(w['calories'] for w in user_workouts)
        user['total_time_hours'] = sum(w['duration'] for w in user_workouts) / 60.0

    sorted_users = sorted(users, key=lambda u: u['total_workouts'], reverse=True)

    print("ТОП-3 АКТИВНЫХ ПОЛЬЗОВАТЕЛЕЙ:")
    for i, user in enumerate(sorted_users[:3], 1):
        print(f"{i}. {user['name']} ({user['fitness_level']}):")
        print(f"   Тренировок: {user['total_workouts']}")
        print(f"   Калорий: {user['total_calories']}")
        print(f"   Время: {user['total_time_hours']:.1f} часов")
        print()
    print()

def analyze_workout_types(workouts: List[Dict[str, Any]]) -> None:
    types = {}
    for w in workouts:
        t = w['type']
        if t not in types:
            types[t] = {'count': 0, 'total_duration': 0, 'total_calories': 0}
        types[t]['count'] += 1
        types[t]['total_duration'] += w['duration']
        types[t]['total_calories'] += w['calories']

    total = len(workouts)
    print("РАСПРЕДЕЛЕНИЕ ПО ТИПАМ ТРЕНИРОВОК:")
    for t, data in types.items():
        percent = (data['count'] / total) * 100
        avg_duration = data['total_duration'] / data['count']
        avg_calories = data['total_calories'] / data['count']
        print(f"{t}: {data['count']} тренировок ({percent:.1f}%)")
        print(f"   Средняя длительность: {avg_duration:.0f} мин")
        print(f"   Средние калории: {avg_calories:.0f} ккал")
    print()

def find_user_workouts(users: List[Dict[str, Any]], workouts: List[Dict[str, Any]], user_name: str) -> List[Dict[str, Any]]:
    user = next((u for u in users if u['name'].lower() == user_name.lower()), None)
    if not user:
        print(f"Пользователь {user_name} не найден.")
        return []
    return [w for w in workouts if w['user_id'] == user['user_id']]

def analyze_user(users: List[Dict[str, Any]], workouts: List[Dict[str, Any]], user_name: str) -> None:
    user = next((u for u in users if u['name'].lower() == user_name.lower()), None)
    if not user:
        print(f"Пользователь {user_name} не найден.")
        return

    user_workouts = find_user_workouts(users, workouts, user_name)
    if not user_workouts:
        print(f"У пользователя {user_name} нет тренировок.")
        return

    total_workouts = len(user_workouts)
    total_calories = sum(w['calories'] for w in user_workouts)
    total_time_hours = sum(w['duration'] for w in user_workouts) / 60.0
    total_distance = sum(w['distance'] for w in user_workouts)
    avg_calories_per_workout = total_calories / total_workouts if total_workouts > 0 else 0

    types_count = {}
    for w in user_workouts:
        t = w['type']
        types_count[t] = types_count.get(t, 0) + 1
    favorite_type = max(types_count, key=types_count.get) if types_count else "нет данных"

    print(f"ДЕТАЛЬНЫЙ АНАЛИЗ ДЛЯ ПОЛЬЗОВАТЕЛЯ: {user['name']}")
    print("=" * 60)
    print(f"Возраст: {user['age']} лет, Вес: {user['weight']} кг")
    print(f"Уровень: {user['fitness_level']}")
    print(f"Тренировок: {total_workouts}")
    print(f"Сожжено калорий: {total_calories}")
    print(f"Общее время: {total_time_hours:.1f} часов")
    print(f"Пройдено дистанции: {total_distance:.1f} км")
    print(f"Средние калории за тренировку: {avg_calories_per_workout:.0f}")
    print(f"Любимый тип тренировки: {favorite_type}")
    print()

def visualize_data(users: List[Dict[str, Any]], workouts: List[Dict[str, Any]]) -> None:
    types_count = {}
    for w in workouts:
        t = w['type']
        types_count[t] = types_count.get(t, 0) + 1

    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.pie(types_count.values(), labels=types_count.keys(), autopct='%1.1f%%')
    plt.title('Распределение типов тренировок')

    user_names = [u['name'] for u in users]
    user_workouts_counts = [len([w for w in workouts if w['user_id'] == u['user_id']]) for u in users]

    plt.subplot(1, 3, 2)
    plt.bar(user_names, user_workouts_counts, color='skyblue')
    plt.title('Активность пользователей (количество тренировок)')
    plt.xticks(rotation=45, ha='right')

    user_avg_calories = []
    for u in users:
        user_ws = [w for w in workouts if w['user_id'] == u['user_id']]
        avg = sum(w['calories'] for w in user_ws) / len(user_ws) if user_ws else 0
        user_avg_calories.append(avg)

    plt.subplot(1, 3, 3)
    plt.bar(user_names, user_avg_calories, color='lightcoral')
    plt.title('Средние калории за тренировку')
    plt.xticks(rotation=45, ha='right')

    plt.tight_layout()
    plt.show()

    user_total_calories = [sum(w['calories'] for w in workouts if w['user_id'] == u['user_id']) for u in users]

    plt.figure(figsize=(10, 6))
    plt.bar(user_names, user_total_calories, color='orange')
    plt.title('Общие затраченные калории по пользователям')
    plt.xlabel('Пользователи')
    plt.ylabel('Калории')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

def main():
    users = load_users_data()
    workouts = load_workouts_data()

    if not users or not workouts:
        print("Не удалось загрузить данные. Проверьте наличие файлов users.xml и workouts.xml.")
        return

    get_stats(users, workouts)

    analyze_user_activity(users, workouts)
    analyze_workout_types(workouts)

    analyze_user(users, workouts, "Борис")

    visualize_data(users, workouts)

if __name__ == "__main__":
    main()