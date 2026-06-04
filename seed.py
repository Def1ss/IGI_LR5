import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'forsazh_fitness.settings')
django.setup()

from django.contrib.auth.models import User
from content.models import News, GlossaryTerm, Vacancy, FAQ
from workouts.models import WorkoutType, GymHall, Group, ScheduledClass
from promocodes.models import PromoCode
from users.models import Client, Instructor
from reviews.models import Review
import datetime
from django.utils import timezone
from content.models import CompanyHistory, CompanyContact

def seed():
    print("Starting database seeding...")
    if User.objects.filter(username='admin').exists():
        print("Seed already exists — skipping")
        return
    # 1. Superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin_forsazh')
        print("Created superuser 'admin' with password 'admin_forsazh'")

    # 2. Instructors & Clients
    if not User.objects.filter(username='trainer_ivan').exists():
        u = User.objects.create_user('trainer_ivan', 'ivan@example.com', 'trainer123', first_name='Иван', last_name='Смирнов')
        Instructor.objects.create(user=u, bio='Опыт 10 лет, мастер спорта по кроссфиту', specialization='Силовые тренировки и Кроссфит')
        print("Created instructor Ivan")
    
    if not User.objects.filter(username='trainer_anna').exists():
        u = User.objects.create_user('trainer_anna', 'anna@example.com', 'trainer123', first_name='Анна', last_name='Козлова')
        Instructor.objects.create(user=u, bio='Сертифицированный тренер по хатха-йоге и стретчингу', specialization='Йога и Растяжка')
        print("Created instructor Anna")

    if not User.objects.filter(username='client_dmitry').exists():
        u = User.objects.create_user('client_dmitry', 'dmitry@example.com', 'client123', first_name='Дмитрий', last_name='Королёв')
        Client.objects.create(user=u, phone='+375 (29) 555-55-55')
        print("Created client Dmitry")

    inst_ivan = Instructor.objects.get(user__username='trainer_ivan')
    inst_anna = Instructor.objects.get(user__username='trainer_anna')
    client_dmitry = Client.objects.get(user__username='client_dmitry')

    # 3. Workout types
    if not WorkoutType.objects.exists():
        wt1 = WorkoutType.objects.create(name='Йога', description='Гармония ума и тела, развитие гибкости и баланса.', price_per_session=15.00, price_per_cycle=150.00, category='group')
        wt2 = WorkoutType.objects.create(name='Кроссфит / HIIT', description='Высокоинтенсивный функциональный тренинг для максимального сжигания калорий и выносливости.', price_per_session=20.00, price_per_cycle=200.00, category='group')
        wt3 = WorkoutType.objects.create(name='Персональная тренировка', description='Индивидуальное занятие с лучшим тренером под ваши цели.', price_per_session=35.00, price_per_cycle=350.00, category='individual')
        print("Seeded WorkoutTypes")

    wt_yoga = WorkoutType.objects.get(name='Йога')
    wt_cross = WorkoutType.objects.get(name='Кроссфит / HIIT')

    # 4. Gym Halls
    if not GymHall.objects.exists():
        GymHall.objects.create(name='Зал А (Главный)', capacity=30, equipment='Силовая рама, гантели, грифы, TRX петли')
        GymHall.objects.create(name='Зал Б (Групповой)', capacity=20, equipment='Коврики для йоги, фитболы, степ-платформы')
        print("Seeded GymHalls")

    hall_a = GymHall.objects.get(name='Зал А (Главный)')
    hall_b = GymHall.objects.get(name='Зал Б (Групповой)')

    # 5. Groups
    if not Group.objects.exists():
        g1 = Group.objects.create(name='Утренняя Йога', workout_type=wt_yoga)
        g1.instructors.add(inst_anna)
        
        g2 = Group.objects.create(name='Вечерний Кроссфит', workout_type=wt_cross)
        g2.instructors.add(inst_ivan)
        print("Seeded Groups")

    group_yoga = Group.objects.get(name='Утренняя Йога')
    group_cross = Group.objects.get(name='Вечерний Кроссфит')

    # 6. Scheduled classes
    if not ScheduledClass.objects.exists():
        now = timezone.now()
        # Monday next week at 9:00
        start1 = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1), datetime.time(9, 0))
        start1 = timezone.make_aware(start1, timezone.get_current_timezone())
        end1 = start1 + datetime.timedelta(hours=1)
        sc1 = ScheduledClass.objects.create(group=group_yoga, hall=hall_b, start_time=start1, end_time=end1)
        sc1.instructor_ids.add(inst_anna)

        start2 = datetime.datetime.combine(datetime.date.today() + datetime.timedelta(days=1), datetime.time(19, 0))
        start2 = timezone.make_aware(start2, timezone.get_current_timezone())
        end2 = start2 + datetime.timedelta(hours=1, minutes=30)
        sc2 = ScheduledClass.objects.create(group=group_cross, hall=hall_a, start_time=start2, end_time=end2)
        sc2.instructor_ids.add(inst_ivan)
        print("Seeded Scheduled Classes")

    # 7. News (Seeding 10 entries)
    if not News.objects.exists():
        News.objects.create(title='Новое оборудование в зале А', slug='new-equipment', summary='Мы закупили профессиональные силовые тренажеры премиум-класса.', full_text='Отличные новости для любителей силовых нагрузок! Зал А пополнился новыми тренажерами от мировых производителей. Попробуйте уже сегодня!', author_name='Администрация', image_url='https://images.unsplash.com/photo-1540497077202-7c8a3999166f?w=600&auto=format&fit=crop')
        News.objects.create(title='Детский фитнес-кэмп', slug='kids-fitness-camp', summary='Открываем набор в летний спортивный лагерь для детей от 7 до 14 лет.', full_text='Программа включает развивающие тренировки, основы плавания, активные игры и правильное здоровое питание под присмотром тренеров.', author_name='Анна Козлова', image_url='https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?w=600&auto=format&fit=crop')
        News.objects.create(title='Летние скидки на карты!', slug='summer-sales-card', summary='Только на этой неделе скидки до 30% на абонементы.', full_text='Приготовьтесь к лету выгодно! Оформите карту в личном кабинете или на ресепшн со значительной скидкой.', author_name='Администрация', image_url='https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=600&auto=format&fit=crop')
        News.objects.create(title='Новый тренер по Пилатесу', slug='novy-trainer-pilates', summary='Приветствуем Елену Смирнову в нашей фитнес-команде.', full_text='Елена Смирнова — опытный тренер со стажем более 10 лет, сертифицированный спец по восстановительному фитнесу.', author_name='Егор Воронов', image_url='https://images.unsplash.com/photo-1518611012118-696072aa579a?w=600&auto=format&fit=crop')
        News.objects.create(title='Режим работы в праздники', slug='holiday-hours', summary='Обратите внимание на график работы 3 июля.', full_text='В праздничный день клуб открыт с 9:00 до 21:00. Групповые занятия проводятся сокращенно.', author_name='Администрация', image_url='https://images.unsplash.com/photo-1507398941214-572c25f4b1dc?w=600&auto=format&fit=crop')
        News.objects.create(title='Кроссфит-марафон 2026', slug='crossfit-marathon-2026', summary='Принимаем заявки на участие в ежегодном марафоне.', full_text='Испытайте выносливость и поборитесь за кубок ФОРСАЖа! Победителю достанется годовая VIP-карта клуба.', author_name='Иван Смирнов', image_url='https://images.unsplash.com/photo-1517840139904-4f06bad15731?w=600&auto=format&fit=crop')
        News.objects.create(title='Мастер-класс по Хатха-Йоге', slug='hatha-yoga-masterclass', summary='Углубленное погружение в практику асан и пранаямы.', full_text='Узнайте тайны правильного дыхания и выстраивания поз на бесплатном интенсиве от Анны Козловой в эту субботу.', author_name='Анна Козлова', image_url='https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=600&auto=format&fit=crop')
        News.objects.create(title='Функциональный тест в зале', slug='functional-fitness-test', summary='Пройдите бесплатную диагностику состава тела у дежурного тренера.', full_text='Узнайте процент жировой и мышечной массы, получите рекомендации по составлению тренировок.', author_name='Администрация', image_url='https://images.unsplash.com/photo-1526506118085-60ce8714f8c5?w=600&auto=format&fit=crop')
        News.objects.create(title='Здоровое питание от нутрициолога', slug='nutrition-talk', summary='Семинар о правильных пищевых привычках.', full_text='Как не срываться на сладкое, правильно рассчитывать КБЖУ и улучшить самочувствие под нагрузками.', author_name='Администрация', image_url='https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=600&auto=format&fit=crop')
        News.objects.create(title='Запуск СПА-зоны и сауны', slug='spa-launch', summary='Наш термальный комплекс полностью обновлен и готов к гостям.', full_text='Приятное расслабление после тренировок! Хаммам, финская сауна и контрастный бассейн для всех обладателей VIP-карт.', author_name='Администрация', image_url='https://images.unsplash.com/photo-1540555700478-4be289fbecef?w=600&auto=format&fit=crop')
        print("Seeded 10 News Articles")

    # 8. Glossary (Seeding 10 entries)
    if not GlossaryTerm.objects.exists():
        GlossaryTerm.objects.create(term='Анаэробный порог (АнП)', category='Физиология', definition='Уровень интенсивности нагрузки, при котором концентрация лактата в крови начинает резко расти.', image_url='https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=400&auto=format&fit=crop')
        GlossaryTerm.objects.create(term='Гипертрофия мышц', category='Анатомия', definition='Процесс увеличения объема мышечных волокон в ответ на регулярные силовые тренировки.', image_url='https://images.unsplash.com/photo-1540497077202-7c8a3999166f?w=400&auto=format&fit=crop')
        GlossaryTerm.objects.create(term='Супинация', category='Биомеханика', definition='Вращательное движение конечности наружу, например поворот кисти ладонью вверх.', image_url='https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?w=400&auto=format&fit=crop')
        GlossaryTerm.objects.create(term='Аэробная выносливость', category='Качества', definition='Способность организма длительно выполнять работу умеренной мощности за счет кислородного окисления.', image_url='https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?w=400&auto=format&fit=crop')
        GlossaryTerm.objects.create(term='Пронация', category='Биомеханика', definition='Вращение конечности внутрь. Для стопы — опускание внутреннего края при наступании.', image_url='https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400&auto=format&fit=crop')
        GlossaryTerm.objects.create(term='Креатинфосфат', category='Биохимия', definition='Высокоэнергетическое вещество, обеспечивающее мгновенную регенерацию АТФ в первые секунды взрывной нагрузки.', image_url='https://images.unsplash.com/photo-1526506118085-60ce8714f8c5?w=400&auto=format&fit=crop')
        GlossaryTerm.objects.create(term='Гибкость', category='Качества', definition='Амплитуда движений в суставах, зависящая от эластичности мышечно-связочного аппарата.', image_url='https://images.unsplash.com/photo-1518611012118-696072aa579a?w=400&auto=format&fit=crop')
        GlossaryTerm.objects.create(term='Метаболизм', category='Физиология', definition='Совокупность всех химических реакций синтеза (анаболизма) и распада (катаболизма) в живом организме.', image_url='https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=400&auto=format&fit=crop')
        GlossaryTerm.objects.create(term='Кроссфит', category='Направления', definition='Круговая система тренировок высокой интенсивности, включающая элементы гиревого спорта, легкой атлетики.', image_url='https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=400&auto=format&fit=crop')
        GlossaryTerm.objects.create(term='Дефицит калорий', category='Питание', definition='Состояние, когда организм тратит больше калорий, чем получает из пищи, запускающее процесс похудения.', image_url='https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=400&auto=format&fit=crop')
        print("Seeded 10 Glossary terms")

    # 9. Promocodes
    if not PromoCode.objects.exists():
        PromoCode.objects.create(code='FORSAZH2026', discount_percent=15, is_active=True, valid_to=datetime.date(2026, 12, 31), applicable_to='Все абонементы')
        PromoCode.objects.create(code='YOGA50', discount_percent=50, is_active=True, valid_to=datetime.date(2026, 7, 1), applicable_to='Групповая йога')
        print("Seeded Promocodes")

    # 10. FAQ
    if not FAQ.objects.exists():
        FAQ.objects.create(question='Нужна ли медицинская справка для посещений?', answer='Да, для вашей безопасности мы настоятельно просим предоставить справку о допуске к занятиям спортом от терапевта.')
        FAQ.objects.create(question='Можно ли вернуть деньги за неиспользованный абонемент?', answer='Да, возврат средств осуществляется согласно договору-оферте за вычетом фактически посещенных дней.')
        print("Seeded FAQ")

    # 11. Vacancies
    if not Vacancy.objects.exists():
        Vacancy.objects.create(position='Инструктор тренажёрного зала', description='Ищем активного тренера с профильным образованием. Проведение вводных тренировок, дежурство в зале.', salary='от 1000 BYN')
        Vacancy.objects.create(position='Администратор рецепции', description='Встреча гостей, консультирование клиентов по услугам, оформление карт, касса.', salary='от 750 BYN')
        print("Seeded Vacancies")

    # 12. Reviews (Seeding 10 entries)
    if not Review.objects.exists():
        Review.objects.create(client=client_dmitry, rating=5, comment='Отличный клуб! Все новое оборудование, чистые раздевалки и вежливый персонал.', is_approved=True)
        Review.objects.create(client=client_dmitry, rating=5, comment='Обожаю групповые занятия по йоге с Анной Козловой! Всегда расслабляющая и приятная атмосфера.', is_approved=True)
        Review.objects.create(client=client_dmitry, rating=4, comment='Качественный силовой зал. Много силовых рам и свободных весов. Вечером бывает многолюдно.', is_approved=True)
        Review.objects.create(client=client_dmitry, rating=5, comment='Иван Смирнов — потрясающий кроссфит-тренер! Нагрузки жесткие, но результат невероятный.', is_approved=True)
        Review.objects.create(client=client_dmitry, rating=5, comment='Очень уютная СПА-зона. Баня и контрастный бассейн после тяжелых подходов — это сказка!', is_approved=True)
        Review.objects.create(client=client_dmitry, rating=5, comment='Прекрасный детский спортивный кэмп летом. Мой ребенок в восторге от бассейна и активных игр.', is_approved=True)
        Review.objects.create(client=client_dmitry, rating=5, comment='Зарегистрировался через сайт быстро, купил абонемент со скидкой по промокоду. Очень удобно.', is_approved=True)
        Review.objects.create(client=client_dmitry, rating=4, comment='Индивидуальные тренировки стоят своих денег. За месяц скорректировал диету.', is_approved=True)
        Review.objects.create(client=client_dmitry, rating=5, comment='Рекомендую клуб всем знакомым. ФОРСАЖ — лучшая атмосфера спорта в нашем районе!', is_approved=True)
        Review.objects.create(client=client_dmitry, rating=5, comment='Всегда чистая питьевая вода в кулерах, удобное расположение, достаточное количество парковочных мест.', is_approved=True)
        print("Seeded 10 Reviews")
    
    #13. CompHist
    if not CompanyHistory.objects.exists():
        CompanyHistory.objects.bulk_create([
            CompanyHistory(
                year=2018,
                event="Основание клуба ФОРСАЖ. Первый небольшой зал.",
                image_url="https://images.unsplash.com/photo-1517836357463-d25dfeac3438"
            ),
            CompanyHistory(
                year=2020,
                event="Открытие кроссфит-зоны и детских программ.",
                image_url="https://images.unsplash.com/photo-1518611012118-696072aa579a"
            ),
            CompanyHistory(
                year=2022,
                event="Расширение клуба до 1200 кв.м и награда года.",
                image_url="https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b"
            ),
            CompanyHistory(
                year=2024,
                event="Внедрение AI-системы отслеживания прогресса.",
                image_url="https://images.unsplash.com/photo-1558611848-73f7eb4001a1"
            ),
        ])
        print("Seeded Company History")


    # 14. Company Contacts
    if not CompanyContact.objects.exists():
        CompanyContact.objects.bulk_create([
            CompanyContact(
                name="Иван Смирнов",
                role="Старший тренер",
                phone="+375 (29) 111-22-33",
                photo_url="https://images.unsplash.com/photo-1560250097-0b93528c311a"
            ),
            CompanyContact(
                name="Анна Петрова",
                role="Администратор",
                phone="+375 (29) 444-55-66",
                photo_url="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2"
            ),
        ])
        print("Seeded Company Contacts")
    
    print("Database seeding completed successfully!")

if __name__ == '__main__':
    seed()
