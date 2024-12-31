import hashlib
from time import sleep


class User:
    def __init__(self, nickname, password, age):
        self.nickname = nickname
        self.password = self._hash_password(password)
        self.age = age

    def _hash_password(self, password):
        return hashlib.sha512(password.encode()).hexdigest()

    def __str__(self):
        return self.nickname

    def __repr__(self):
        return f"User(nickname={self.nickname}, age={self.age})"


class Video:
    def __init__(self, title, duration, adult_mode=False):
        self.title = title
        self.duration = duration
        self.adult_mode = adult_mode

    def __str__(self):
        return self.title

    def __repr__(self):
        return f"Video(title={self.title}, duration={self.duration}, adult_mode={self.adult_mode})"


class UrTube:
    def __init__(self):
        self.users = {}
        self.videos = {}
        self.current_user = None

    def log_in(self, nickname, password):
        user = self.users.get(nickname)
        if user and user.password == hashlib.sha512(password.encode()).hexdigest():
            self.current_user = user
        else:
            print("Неверный логин или пароль")

    def register(self, nickname, password, age):
        if nickname in self.users:
            print(f"Пользователь {nickname} уже существует")
            return
        self.users[nickname] = User(nickname, password, age)
        self.current_user = self.users[nickname]

    def log_out(self):
        self.current_user = None

    def add(self, *videos):
        for video in videos:
            if video.title not in self.videos:
                self.videos[video.title] = video

    def get_videos(self, search_word):
        search_word_lower = search_word.lower()
        return [title for title in self.videos if search_word_lower in title.lower()]

    def watch_video(self, movie_title):
        if not self.current_user:
            print("Войдите в аккаунт, чтобы смотреть видео")
            return

        video = self.videos.get(movie_title)
        if not video:
            print("Видео не найдено")
            return

        if video.adult_mode and self.current_user.age < 18:
            print("Вам нет 18 лет, пожалуйста покиньте страницу")
            return

        for second in range(video.duration):
            print(f"Секунда: {second + 1}")
            sleep(0.5)

        print("Конец видео")


ur = UrTube()
v1 = Video("Лучший язык программирования 2024 года", 200)
v2 = Video("Для чего девушкам парень программист?", 10, adult_mode=True)

# Добавление видео
ur.add(v1, v2)

# Проверка поиска
print(ur.get_videos("лучший"))
print(ur.get_videos("ПРОГ"))

# Проверка на вход пользователя и возрастное ограничение
ur.watch_video("Для чего девушкам парень программист?")
ur.register("vasya_pupkin", "lolkekcheburek", 13)
ur.watch_video("Для чего девушкам парень программист?")
ur.register("urban_pythonist", "iScX4vIJClb9YQavjAgF", 25)
ur.watch_video("Для чего девушкам парень программист?")

# Проверка входа в другой аккаунт
ur.register("vasya_pupkin", "F8098FM8fjm9jmi", 55)
print(ur.current_user)

# Попытка воспроизведения несуществующего видео
ur.watch_video("Лучший язык программирования 2024 года!")
