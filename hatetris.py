from typing import List

import numpy as np
import random
from tetrimino import Tetrimino
from field import Field


class Hatetris:
    """Hatetris AI"""

    def __init__(self):
        self.past_area = []

    def add_field(self, field):
        self.past_area.append(field.get_bit_field())

    @staticmethod
    def _generate_tetrimino(type=None):
        """テトリミノをランダムに1つ生成する関数

        :return: ランダムに生成されたTetrimino インスタンス
        """
        random.seed()
        if type is None:
            type = random.randrange(0, 7)
        return Tetrimino(5, 2, 0, type)

    @staticmethod
    def get_candidate_list(init_mino, field):
        """ 盤面の状況を踏まえて落下可能なテトリミノ候補をすべて返す

        :param init_mino: 与えられたテトリミノ
        :param field: 盤面
        :return: 落下可能な位置にあるテトリミノ配列 (落下の高さに応じてscore値をセットする)
        """
        candidate = []
        rotete_num = 1
        mino_type = init_mino.get_type()

        # タイプによって回転のバリエーションが2 or 4 となる
        if 1 <= mino_type <= 3:
            rotete_num = 2
        if mino_type >= 4:
            rotete_num = 4

        # 各回転パターンに応じて
        for i in range(rotete_num):
            mino = init_mino.clone(0, 0, i)

            # まずは最も左に寄せる
            while True:
                next_mino = mino.clone(-1, 0, 0)
                if next_mino.collision(field):
                    break
                mino = next_mino
            base_mino = mino

            while True:
                mino = base_mino
                score = 0
                while True:
                    # 可能なところまで落下させる
                    next_mino = mino.clone(0, 1, 0)
                    if next_mino.collision(field):
                        break
                    mino = next_mino
                    score += 1
                mino.set_score(score)
                candidate.append(mino)

                # １つづつ右に移動させる
                next_mino = base_mino.clone(1, 0, 0)
                if next_mino.collision(field):
                    break
                base_mino = next_mino
        return candidate

    @staticmethod
    def get_next_state(field: Field, mino: Tetrimino, move: str) -> (Field, Tetrimino):
        """ 次の状態を返す

        :param field: 盤面
        :param mino: テトリミノ
        :param move: 次の動作: L: 左に移動, R: 右に移動, D: 下に移動, R: 右に回転
        :return: 次の状態
        """
        next_mino = mino.clone()
        if move == 'L':
            next_mino = mino.clone(-1, 0, 0)
        elif move == 'R':
            next_mino = mino.clone(1, 0, 0)
        elif move == 'D':
            next_mino = mino.clone(0, 1, 0)
        elif move == 'U':
            next_mino = mino.clone(0, 0, 1)
        else:
            raise ValueError('Invalid move')

        if next_mino.collision(field):
            return mino, bool(move == 'D')
        else:
            return next_mino, False
        #     if move == 'D':
        #         # lock
        #         next_field.set_blocks(mino.get_blocks())
        #         next_mino = None
        #
        #     else:
        #         # no move
        #         next_mino = mino
        #         next_field.set_blocks(next_mino.get_blocks())
        # return next_mino, is_locked

    def get_next_core_states(self, field: Field, init_mino: Tetrimino) -> List[Tetrimino]:
        """
        :param field: 盤面
        :param mino_type: テトリミノのタイプ
        :return:
        """
        # field_flame = Field()
        mino = init_mino.clone(0, 0, 0)
        while True:
            base_mino = mino.clone(0, 1, 0)
            has_block = False
            y = base_mino.y + 4
            f, _ = field.next_field(base_mino.get_blocks())
            if f is False:
                break
            for i in range(1, 11):
                if f.tiles[y][i] != -1:
                    has_block = True
                    continue
            if base_mino.collision(field) or has_block:
                break
            mino = base_mino
        mino_positions = [mino]
        candidates = []
        seen = set()
        seen.add(hash(base_mino))
        i = 0
        while i < len(mino_positions):
            m = mino_positions[i]
            # それぞれの操作に対して捜査
            for c in ['L', 'R', 'U', 'D']:
                next_mino, is_locked = self.get_next_state(field, m, c)
                if is_locked:
                    candidates.append(next_mino)
                else:
                    if hash(next_mino) not in seen:
                        mino_positions.append(next_mino)
                        seen.add(hash(next_mino))
            i += 1
        return candidates

    def generate_worst_tetrimino(self, field):
        """ 最もスコアの低い落下位置を計算する

        :param field
        :return: 落下後の盤面のスコアが最も低いテトリミノ
        """
        # mino list is sorted by priority S -> Z -> O -> I -> L -> J -> T
        mino_rank_list = [2, 3, 0, 1, 5, 4, 6]
        mino_obj_list = [self._generate_tetrimino(i) for i in mino_rank_list]
        mino_cycle_list = []
        mino_score_list = []
        # append the current field state
        self.add_field(field)
        for mino in mino_obj_list:
            candidates = self.get_next_core_states(field, mino)
            has_seen = False
            max_score = np.NINF
            for m in candidates:
                f, _ = field.next_field(m.get_blocks())
                if not f:
                    continue
                bit_field = f.get_bit_field()
                # check the bit field is already exist (it means potentially lead into a previous state)
                if bit_field in self.past_area:
                    has_seen = True
                # get field score
                field_score = f.get_field_score()
                # get most high block's height
                height = field_score[7]
                # set score as value of height
                s = 16 - height
                if field_score[0] == 0:
                    s = field_score[6]
                if max_score < s:
                    max_score = s
            mino_cycle_list.append(int(has_seen))
            mino_score_list.append(max_score)

        # get mino which has the worst best-case scenario for the player
        mino_dict = [{'type': mino_rank_list[i],
                      'rank': i,
                      'cycle': mino_cycle_list[i],
                      'score': mino_score_list[i]} for i in range(len(mino_rank_list))]
        sort = sorted(mino_dict, key=lambda x: (x['cycle'], x['score'], x['rank']))
        worst_mino = sort[0]['type']
        return self._generate_tetrimino(worst_mino)


if __name__ == "__main__":
    h = Hatetris()
    f = Field()
    f.tiles[18] = [9, -1, 2, 2, -1, -1, 2, 2, -1, -1, -1, 9]
    f.tiles[19] = [9, 2, 2, -1, -1, 2, 2, -1, -1, -1, -1, 9]
    m1 = h.get_candidate_list(h._generate_tetrimino(1), f)
    m2 = h.get_next_core_states(f, h._generate_tetrimino(1))
    print(m1)
    print(m2)