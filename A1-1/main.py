"""리스트와 딕셔너리로 관리하는 메모리 기반 프롬프트 보관함."""


CATEGORIES = ['텍스트 생성', '이미지 생성', '영상 생성', '페르소나', '자동화', '기타']


def create_initial_prompts() -> list[dict]:
    """사용자 요청으로 작성한 예시 데이터. 실행할 때마다 새로 만든다."""
    return [
        {
            'title': '파이썬 학습 내용 요약',
            'content': (
                '당신은 파이썬 입문자를 가르치는 튜터입니다. 내가 제공하는 학습 내용을 '
                '핵심 개념 3개, 쉬운 코드 예제, 확인 문제 2개로 정리해주세요. '
                '어려운 용어는 풀어서 설명하고 제공되지 않은 사실은 추측하지 마세요.'
            ),
            'category': '텍스트 생성',
            'favorite': False,
        },
        {
            'title': '독서 앱 홍보 이미지',
            'content': (
                '독서 기록 앱의 홍보용 정사각형 이미지를 만들어주세요. 따뜻한 크림색 배경에 '
                '펼친 책과 작은 화분을 배치하고 부드러운 자연광을 표현해주세요. '
                '위쪽에는 제목을 넣을 여백을 남기고 이미지 안에는 글자를 넣지 마세요.'
            ),
            'category': '이미지 생성',
            'favorite': False,
        },
        {
            'title': '친절한 모의 면접관',
            'content': (
                '당신은 주니어 개발자 면접관입니다. 먼저 지원 직무를 물어보고, '
                '답변을 받은 뒤 관련 질문을 한 번에 하나씩 해주세요. 각 답변마다 '
                '잘한 점 한 가지와 개선할 점 한 가지를 구체적으로 알려주세요. '
                '모르는 내용은 함께 확인할 수 있도록 안내해주세요.'
            ),
            'category': '페르소나',
            'favorite': False,
        },
    ]


def read_required_text(label: str) -> str:
    while True:
        value = input(label).strip()
        if value:
            return value
        print('빈 값은 입력할 수 없습니다. 다시 입력해주세요.')


def select_category() -> str:
    print('카테고리 선택:')
    for number, category in enumerate(CATEGORIES, start=1):
        print(f'{number}) {category}')
    while True:
        choice = input('선택: ').strip()
        # 문자열로 비교해 숫자가 아닌 입력도 예외 없이 처리한다.
        for number, category in enumerate(CATEGORIES, start=1):
            if choice == str(number):
                return category
        print('잘못된 카테고리 번호입니다. 다시 선택해주세요.')


def add_prompt(prompts: list[dict]) -> None:
    print('\n=== 프롬프트 추가 ===')
    title = read_required_text('제목: ')
    content = read_required_text('내용: ')
    category = select_category()
    prompts.append({
        'title': title,
        'content': content,
        'category': category,
        'favorite': False,
    })
    print('프롬프트가 추가되었습니다!')


def print_prompt_list(items: list[tuple[int, dict]]) -> None:
    if not items:
        print('프롬프트가 없습니다.')
        return
    for number, prompt in items:
        star = ' ⭐' if prompt['favorite'] else ''
        print(f"{number}. [{prompt['category']}] {prompt['title']}{star}")
    print(f'총 {len(items)}개의 프롬프트')


def show_list(prompts: list[dict]) -> None:
    print('\n=== 프롬프트 목록 ===')
    print_prompt_list(list(enumerate(prompts, start=1)))


def show_menu() -> None:
    print('\n=== 나만의 프롬프트 관리 ===')
    print('1. 프롬프트 추가')
    print('2. 프롬프트 목록')
    print('3. 카테고리별 조회')
    print('4. 프롬프트 검색')
    print('5. 프롬프트 상세 보기')
    print('6. 즐겨찾기 관리')
    print('7. 즐겨찾기 목록')
    print('0. 종료')


def main() -> None:
    prompts = create_initial_prompts()
    while True:
        show_menu()
        choice = input('선택: ').strip()
        if choice == '0':
            print('프로그램을 종료합니다.')
            break
        elif choice == '1':
            add_prompt(prompts)
        elif choice == '2':
            show_list(prompts)
        elif choice in ('3', '4', '5', '6', '7'):
            print('준비 중인 기능입니다.')
        else:
            print('잘못된 메뉴 번호입니다. 다시 선택해주세요.')


if __name__ == '__main__':
    main()
