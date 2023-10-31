from django.shortcuts import render, redirect, get_object_or_404
from random import *
from .models import Event, DefaultLuckyItem, LuckyItem, DefaultWeapon, Weapon, Character, Enemy
from .forms import CharacterForm
from django.views.decorators.http import require_POST
from django.db.models import Sum

def default_lucky_item_generate():
    lucky_items = {
        '삼각김밥': 2,
        '라면': 5,
        '떡볶이': 8,
        '치킨': 10,
    }
    for lucky_item_name, lucky_item_power in lucky_items.items():
        if DefaultLuckyItem.objects.filter(name=lucky_item_name).count() == 0:
            DefaultLuckyItem.objects.create(
                name = lucky_item_name,
                power = lucky_item_power,
            )

def default_weapon_generate():
    weapons = {
        '주먹도끼': 2,
        '가벼운 물총': 3,
        '낡은 검': 5,
        '수상한 막대기': 7,
        '수학의 정석': 9,
    }
    for weapon_name, weapon_power in weapons.items():
        if DefaultWeapon.objects.filter(name=weapon_name).count() == 0:
            DefaultWeapon.objects.create(
                name = weapon_name,
                power = weapon_power,
            )

def default_enemy_generate():
    enemies = {
        # 종이 시리즈
        '흩날리는 종이': [1, 10],
        '흩날리는 유인물': [1, 15],
        '흩날리는 학습지': [2, 30],
        '흩날리는 시험지': [2, 100],
        '중간고사': [3, 330],
        '기말고사': [4, 440],
        '모의고사': [5, 550],
        '대학수학능력시험': [7, 770],
        '전공시험': [9, 990],
        '졸업논문': [10, 1500],

        # 과제 시리즈
        '수행평가': [3, 250],
        '개별과제': [8, 750],
        '조별과제': [8, 1000],

        # 공식 시리즈
        '국어 문법': [1, 80],
        '수학 공식': [1, 85],
        '영어 문법': [1, 85],
        '피타고라스 정리': [2, 165],
        '이진법': [2, 175],
        '옴의 법칙': [2, 185],
        '미적분': [5, 485],
        
        # 주방용품 시리즈
        '뒤집어진 냄비': [1, 25],
        '코팅이 벗겨진 후라이팬': [2, 125],
        '비어있는 냄비': [3, 225],
        '코팅 후라이팬': [4, 325],
        '달궈진 후라이팬': [5, 425],
        '끓고있는 냄비': [5, 445],

        # 버섯 시리즈
        '수수한 독버섯': [1, 50],
        '화려한 독버섯': [2, 150],
        
        # 용 시리즈
        '아기 용': [1, 100],
        '드래곤 헤츨링': [3, 300],
        '성룡': [6, 600],
        '투명 드래곤': [8, 800],
        '고대룡': [10, 1000],
    }
    for enemy_name, enemy_info in enemies.items():
        if Enemy.objects.filter(name=enemy_name).count() == 0:
            Enemy.objects.create(
                name = enemy_name,
                level = enemy_info[0],
                hp = enemy_info[1],
            )

def default_event_generate():
    if Event.objects.all().count() == 0:
        event_order = 1
    else:
        latest_event = Event.objects.last()
        event_order = latest_event.order + 1

    events_and_lucky_items = {
        '오픈 기념 이벤트': [
            True,
            {
                '행운의 꽃다발': [1, 50],
            },
        ],
        '수능 이벤트': [
            False,
            {
                '수능 샤프': [1, 30],
            },
        ],
    }

    for event_title, event_lucky_items in events_and_lucky_items.items():
        if Event.objects.filter(title=event_title).count() == 0:
            Event.objects.create(
                order = event_order,
                title = event_title,
                active = event_lucky_items[0],
            )
            event_order += 1
        
        event = Event.objects.get(title=event_title)
        for event_lucky_item_name, event_lucky_item_info in event_lucky_items[1].items():
            if DefaultLuckyItem.objects.filter(event__title=event_title, name=event_lucky_item_name).count() == 0:
                DefaultLuckyItem.objects.create(
                    name = event_lucky_item_name,
                    power = event_lucky_item_info[1],
                    event = event,
                    max_level = event_lucky_item_info[0],
                )

def game_list(request):
    default_lucky_item_generate()
    default_weapon_generate()
    default_enemy_generate()
    default_event_generate()
    return render(request, 'games/game_list.html')

def adventure_home(request):
    # 로그인 한 경우
    if request.user.is_authenticated:
        # 생성한 캐릭터가 없을 경우
        if Character.objects.filter(user=request.user).count() == 0:
            if request.method == 'POST':
                character_form = CharacterForm(request.POST)
                character_form = character_form.save(commit=False)
                character_form.user = request.user
                character_form.save()
                return redirect('games:adventure_home')
            else:
                character_form = CharacterForm()
            context = {
                'character_form': character_form,
            }
            return render(request, 'games/character_form.html', context)
        # 생성한 캐릭터가 있는 경우
        else:
            character = get_object_or_404(Character, user=request.user)
            # 무기를 얻지 못한 경우
            if character.weapon == None:
                # 무기 랜덤 선택
                random_weapon = DefaultWeapon.objects.filter(event=None).order_by('?')[0]
                context = {
                    'random_weapon': random_weapon,
                }
                return render(request, 'games/adventure_new.html', context)
            # 무기를 얻은 경우
            else:
                context = {
                    'character': character,
                    'weapon_name': character.weapon.default_weapon.name,
                    'weapon_power': character.weapon.power,
                }
                return render(request, 'games/adventure_home.html', context)
    # 로그인 하지 않은 경우
    else:
        return redirect('accounts:login')

@require_POST
def weapon_get(request):
    character = get_object_or_404(Character, user=request.user)

    weapon_id = request.POST.get('random-weapon')
    selected_weapon = get_object_or_404(DefaultWeapon, id=weapon_id)

    weapon = Weapon.objects.create(
        default_weapon = selected_weapon,
        power = selected_weapon.power
    )
    
    character.weapon = weapon
    character.save()
    return redirect('games:adventure_home')

def adventure_attack(request):
    character = get_object_or_404(Character, user=request.user)
    character_weapon_level = character.weapon.level
    random_enemy = Enemy.objects.filter(level__lte=character_weapon_level).order_by('?')[0]
    
    context = {
        'random_enemy': random_enemy,
    }
    return render(request, 'games/adventure_attack.html', context)

@require_POST
def adventure_attack_result(request):
    character = get_object_or_404(Character, user=request.user)

    enemy_id = request.POST.get('random-enemy')
    enemy = get_object_or_404(Enemy, id=enemy_id)

    if character.weapon.power*10 >= enemy.hp:
        result = '승리'
        reward_coin = randint(enemy.hp*10-enemy.level*5, enemy.hp*10+enemy.level*5)
        character.coin += reward_coin
        character.save()
    else:
        result = '패배'
        reward_coin = 0
    
    context = {
        'enemy': enemy,
        'result': result,
        'reward_coin' : reward_coin,
    }
    return render(request, 'games/adventure_attack_result.html', context)

def weapon_workroom(request):
    character = get_object_or_404(Character, user=request.user)

    # 무기 강화에 필요한 코인 계산 (무기 레벨에 따라 증가)
    required_coin = character.weapon.level*1000

    inventory = character.inventory.all()

    original_power = character.weapon.power
    additional_power = inventory.aggregate(Sum('power'))['power__sum']
    if additional_power == None:
        additional_power = 0

    context = {
        'character': character,
        'weapon_name': character.weapon.default_weapon.name,
        'weapon_level': character.weapon.level,
        'weapon_power': original_power + additional_power,
        'inventory': inventory,
        'original_power': original_power,
        'additional_power': additional_power,
        'required_coin': required_coin,
    }
    return render(request, 'games/weapon_workroom.html', context)

@require_POST
def weapon_pick(request):
    character = get_object_or_404(Character, user=request.user)
    # 캐릭터가 갖고 있는 코인 저장
    character_coin = character.coin
    
    # 캐릭터가 500코인 이상 갖고 있는 경우
    if character_coin >= 500:
        # 500코인 소모
        character.coin = character_coin - 500
        character.save()

        inventory = character.inventory.all()

        original_power = character.weapon.power
        additional_power = inventory.aggregate(Sum('power'))['power__sum']
        if additional_power == None:
            additional_power = 0

        context = {
            'character': character,
            'weapon_name': character.weapon.default_weapon.name,
            'weapon_level': character.weapon.level,
            'weapon_power': original_power + additional_power,
            'inventory': inventory,
            'original_power': original_power,
            'additional_power': additional_power,
        }

        result = choices(['무기', '아이템'], [9, 1])[0]
        get_event = choices([True, False], [3, 7])[0]
        if result == '무기':
            if Event.objects.filter(active=True).count() != 0 and get_event == True and DefaultWeapon.objects.filter(event__active=True).count() != 0:
                random_weapon = DefaultWeapon.objects.filter(event__active=True).order_by('?')[0]
            else:
                random_weapon = DefaultWeapon.objects.filter(event=None).order_by('?')[0]
            context['random_weapon'] = random_weapon
            print(context)
            return render(request, 'games/weapon_change.html', context)
        else:
            if Event.objects.filter(active=True).count() != 0 and get_event == True and DefaultLuckyItem.objects.filter(event__active=True).count() != 0:
                default_random_lucky_item = DefaultLuckyItem.objects.filter(event__active=True).order_by('?')[0]
            else:
                default_random_lucky_item = DefaultLuckyItem.objects.filter(event=None).order_by('?')[0]
            
            # inventory에 default_random_lucky_item의 키를 가진 아이템을 보유하지 않고 있다면
            if character.inventory.filter(default_lucky_item=default_random_lucky_item).count() == 0:
                random_lucky_item = LuckyItem.objects.create(
                    default_lucky_item = default_random_lucky_item,
                    power = default_random_lucky_item.power,
                )
                character.inventory.add(random_lucky_item)
                context['first'] = True
                context['weapon_power'] += random_lucky_item.power
                context['additional_power'] += random_lucky_item.power
            else:
                random_lucky_item = character.inventory.filter(default_lucky_item=default_random_lucky_item)[0]
                limit_level = default_random_lucky_item.max_level
                if random_lucky_item.level < limit_level:
                    random_lucky_item.power += 5
                    random_lucky_item.level += 1
                    random_lucky_item.save()
                    context['upgrade'] = True
                    context['weapon_power'] += 5
                    context['additional_power'] += 5
                
            context['random_lucky_item'] = random_lucky_item
            return render(request, 'games/lucky_item_change.html', context)
    return redirect('games:weapon_workroom')

@require_POST
def weapon_change(request):
    character = get_object_or_404(Character, user=request.user)

    # 기존 무기 제거
    existing_weapon = get_object_or_404(Weapon, id=character.weapon.id)
    existing_weapon.delete()

    # 랜덤으로 선택된 무기 id 가져오기
    weapon_id = request.POST.get('random-weapon')
    selected_weapon = get_object_or_404(DefaultWeapon, id=weapon_id)

    # 새로운 무기 생성
    weapon = Weapon.objects.create(
        default_weapon = selected_weapon,
        power = selected_weapon.power + randint(-1, 1),
    )

    # 캐릭터에 새 무기 장착
    character.weapon = weapon
    character.save()

    return redirect('games:weapon_workroom')

@require_POST
def weapon_upgrade(request):
    character = get_object_or_404(Character, user=request.user)
    character_weapon_level = character.weapon.level
    # 무기 레벨이 10 이하일 경우에만 강화 가능
    if character_weapon_level < 10:
        # 캐릭터가 갖고 있는 코인 저장
        character_coin = character.coin
        # 무기 강화에 필요한 코인 계산 (무기 레벨에 따라 증가)
        required_coin = character_weapon_level*1000

        # 캐릭터가 무기 강화에 필요한 코인보다 많이 갖고 있으면서 POST 방식으로 요청이 들어온 경우
        if character_coin >= required_coin:

            # 무기 강화에 필요한 코인 소모
            character.coin = character_coin - required_coin
            character.save()

            result = choices(['성공', '실패'], [10-character_weapon_level, character_weapon_level])[0]
            if result == '성공':
                character_weapon = character.weapon
                # 파워 변경 추가
                character_weapon.power += randint(6, 12)
                character_weapon.level += 1
                character_weapon.save()

            inventory = character.inventory.all()

            original_power = character.weapon.power
            additional_power = inventory.aggregate(Sum('power'))['power__sum']
            if additional_power == None:
                additional_power = 0

            context = {
                'character': character,
                'weapon_name': character.weapon.default_weapon.name,
                'weapon_level': character.weapon.level,
                'weapon_power': original_power + additional_power,
                'inventory': inventory,
                'original_power': original_power,
                'additional_power': additional_power,
                'result': result,
            }
            return render(request, 'games/weapon_upgrade.html', context)
    return redirect('games:weapon_workroom')
