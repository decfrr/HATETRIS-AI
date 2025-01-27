import pygame
import sys
import random
from field import Field
from hatetris import Hatetris
from tetrimino import Tetrimino
from config import BLOCK_SIZE, BLOCK_IMG_SIZE

from replay_codecs.codec import encode


def make_colors():
    """7色のブロックをそれぞれ抽出する関数

    tile.png に 40x280の画像があり、40x40で切り出し、最終的には20x20でリサイズ
    :return: 7色のブロック画像配列 (pygame.Surface オブジェクト)
    """
    colors = []
    image = pygame.image.load("./tile.png")
    for i in range(7):
        tmp_color_surface = pygame.Surface((BLOCK_IMG_SIZE, BLOCK_IMG_SIZE))
        color_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
        tmp_color_surface.blit(image, (0, 0), (BLOCK_IMG_SIZE * i, 0, BLOCK_IMG_SIZE, BLOCK_IMG_SIZE))
        pygame.transform.scale(tmp_color_surface, (BLOCK_SIZE, BLOCK_SIZE), color_surface)
        colors.append(color_surface)
    return colors


def generate_tetrimino(type=None):
    """テトリミノをランダムに1つ生成する関数

    :return: ランダムに生成されたTetrimino インスタンス
    """
    random.seed()
    if type is None:
        type = random.randrange(0, 7)
    return Tetrimino(5, 2, 0, type)


def play():
    """ Play関数

    キーボード操作でテトリスを遊べる関数
    :return:
    """
    pygame.init()  # pygameを初期化数する
    screen = pygame.display.set_mode((640, 480))  # 画面サイズを640, 480に
    pygame.display.set_caption("tetris_ai")
    clock = pygame.time.Clock()  # フレームレート(描画頻度)を更新するためのタイマー
    font = pygame.font.SysFont("Arial", 20)

    # イベントの保管リスト
    events_list = []

    # 7色ブロックの準備
    colors = make_colors()

    # 盤面の定義
    field = Field()

    # HateTetrisの定義
    hatetris = Hatetris()
    # 1つめ(初期)のTetrimino(mino)
    mino = hatetris.generate_worst_tetrimino(field)

    # minoの落下が確定して次のminoを生成する必要がある場合にTrueとする
    generate_flag = False

    # ゲームオーバの場合にTrue
    game_over_flag = False

    # トータル経過フレーム数
    num_frame = 0

    # 得点(消したライン数)
    score = 0
    while True:   # ゲームのメインループ
        num_frame += 1
        screen.fill((0, 0, 0))  # マイループで画面を真っ黒に一度する

        # 盤面の描画
        field.draw(screen, colors)
        mino.draw(screen, colors)

        moved_flag = False # キー操作等によりminoが移動したことを表すflag
        for event in pygame.event.get():  # イベントは一括で取得
            if event.type == pygame.QUIT: # 終了ボタンを押したときにpygameを閉じるのはお作法
                print(encode(events_list))
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:  # これよりキーボードのイベントを捕捉
                if event.key == pygame.K_RIGHT:  # 右が押された場合...
                    events_list.append('R')
                    next_mino = mino.clone(1, 0, 0)  # 右に移動したminoを仮に作成
                    if not next_mino.collision(field):  # 当たり判定
                        mino = next_mino  # 当たり判定無しであれば移動確定
                        moved_flag = True
                if event.key == pygame.K_LEFT:
                    events_list.append('L')
                    next_mino = mino.clone(-1, 0, 0)  # 左に移動したminoを仮に作成(以下同様)
                    if not next_mino.collision(field):
                        mino = next_mino
                        moved_flag = True
                if event.key == pygame.K_UP:
                    events_list.append('U')
                    next_mino = mino.clone(0, 0, 1)  # 1回転したminoを仮に作成(時計回り)(以下同様)
                    if not next_mino.collision(field):
                        mino = next_mino
                        moved_flag = True
                if event.key == pygame.K_DOWN:  # 下に移動(落下)は盤面的に可能なところまで落ちる
                    events_list.append('D')
                    next_mino = mino.clone(0, 1, 0)
                    if not next_mino.collision(field):  # 1ブロックづつ落下させ当たり判定を繰り返す
                        mino = next_mino
                        # next_mino = mino.clone(0, 1, 0)
                    else:
                        field.set_blocks(mino.get_blocks())  # 当たり判定があればminoを盤面に固定
                        # y = 3 にブロックがないか確認する
                        for x in range(1, 11):
                            if field.get_tile(x, 3) != -1:
                                game_over_flag = True
                                break
                        if game_over_flag:
                            continue
                        s = field.line_erase()  # 消去可能なラインがあれば消去
                        if s != 0:
                            score += s
                            print("score: {}".format(score))
                        generate_flag = True
                if event.key == pygame.K_SPACE:
                    pass

        if game_over_flag:  # game overであれば何もしない
            print(encode(events_list))
            continue

        if moved_flag:  # キー操作(左右、回転）があった場合は 一旦その移動を完了し落下は次フレームでやる (落下は除く)
            continue

        # next_mino = mino.clone(0, 1, 0)  # minoを下に1つずらしてみる
        # if next_mino.collision(field):  # 盤面との接触判定
        #     field.set_blocks(mino.get_blocks())  # 盤面にブロックを置く(落下停止)
        #     s = field.line_erase()
        #     if s != 0:
        #         score += s
        #         print("Score: {}".format(score))
        #     generate_flag = True
        # else:
        #     mino = next_mino  # 盤面との接触が無いので下に1つ移動を確定する

        if generate_flag:
            has_block = False
            for x in range(1, 11):
                if field.get_tile(x, 3) != -1:
                    has_block = True
                    break
            mino = hatetris.generate_worst_tetrimino(field)
            if mino.collision(field) or has_block:
                print("GAME OVER")
                game_over_flag = True
            generate_flag = False

        pygame.display.update()  # 描画を更新する
        clock.tick(30)  # フレームレートを3 (秒間3回更新するぐらいの頻度に設定)




if __name__ == "__main__":
    play()
