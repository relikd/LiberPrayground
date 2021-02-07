#!/usr/bin/env python3
import LP

SOLVER = LP.VigenereSolver()  # VigenereSolver, AffineSolver, AutokeySolver
SOLVER.input.load(file=LP.path.root('_input.txt'))


def main():
    help_str = '''
Welcome pilgrim,

Available commands are:
 a : Generate all 29 rotations of a given rune-word (a) or inverted rune (ai)
 d : Get decryption key (substitution) for a single phrase
 f : Find words with a given length (f 4, or f word)
 g : Print Gematria Primus (gp) or reversed Gematria (gpr)
 h : Highlight occurrences of interrupt jumps (hj) or reset (h)
 k : Re/set decryption key (k), invert key (ki),
   ': change key shift (ks), rotation (kr), offset (ko), or after padding (kp)
   ': set key jumps (kj) e.g., [1,2] (first appearence of ᚠ is index 1)
 l : Toggle log level: normal (ln), quiet (lq) verbose (lv)
 p : Prime number and emirp check
 t : Translate between runes, text, and indices (0-28)
 x : Execute decryption. Also: load data into memory
   ': set manually (x DATA) or load from file (xf p0-2) (default: _input.txt)
   ': limit/trim loaded data up to nth character (xl 300)

 ? : Show currently set variables
 q : Quit
'''
    print(help_str)
    while True:
        try:
            inpt = input('$>: ').strip()
            if not inpt:
                continue
            cmd_p = inpt.split(' ', 1)
            cmd = cmd_p[0].strip().lower()
            args = cmd_p[1].strip() if len(cmd_p) > 1 else ''

            if cmd[0] != 'l':  # only log mode allowed after find operation
                SOLVER.reset_highlight()

            if cmd == 'help':
                print(help_str)
            elif cmd == 'q' or cmd == 'exit' or cmd == 'quit':
                exit()
            elif cmd == '?':
                print(SOLVER)
            else:
                cmdX = {'a': command_a, 'd': command_d, 'f': command_f,
                        'g': command_g, 'h': command_h, 'k': command_k,
                        'l': command_l, 'p': command_p, 't': command_t,
                        'x': command_x}
                res = cmdX[cmd[0]](cmd, args) if cmd[0] in cmdX else False
                if res is False:
                    print('Command not found.')
        except Exception as e:
            print(e)


# this allow you to write `ks3` instead of `ks 3`
def get_cmd_int(cmd, args, desc=None, start=2):
    val = int(args) if args else 0
    if not val and cmd[start:]:
        val = int(cmd[start:])
    if desc:
        print(f'set {desc}: {val}')
    return val


#########################################
#                  A
#########################################

def command_a(cmd, args):  # [a]ll variations
    if cmd.strip('aliq'):
        return False
    if not args:
        raise Warning('No input provided.')
    root = LP.RuneText(args)
    inclIndex = 'q' not in cmd
    if 'i' in cmd:
        root = ~root
    for i in range(29):
        print('{:02d}: {}'.format(i, (root + i).description(index=inclIndex)))


#########################################
#                  D
#########################################

def command_d(cmd, args):  # [d]ecrypt or single substitution
    if not (cmd in 'decrypt'):
        return False
    if not args:
        trythis = input('What is the encrypted text?: ').strip()
    else:
        trythis = args
    enc = LP.RuneText(trythis)
    print('encrypted:', enc.description())
    target = input('What should the decrypted clear text be?: ').strip()
    plain = LP.RuneText(target)
    print('plaintext:', plain.description())
    if len(enc) != len(plain):
        print('Error: key length mismatch')
    else:
        print('Substition:')
        print((enc.zip_sub(plain)).description())


#########################################
#                  F
#########################################

def command_f(cmd, args):  # (f)ind word
    if not (cmd in 'find'):
        return False
    if not args:
        raise Warning('No input provided.')
    try:
        search_term = None
        s_len = int(args.strip())  # search words with n-length
    except ValueError:
        search_term = LP.RuneText(args)
        s_len = len(search_term)

    cur_words = SOLVER.highlight_words_with_len(s_len)
    SOLVER.run()
    print()
    print('Found:')
    for _, _, pos, _, w in cur_words:
        print(f'{pos:04}: {w.description(count=True)}')
    if search_term:
        print()
        keylen = [len(search_term)]
        if SOLVER.substitute_supports_keylen():
            try:
                inp = input('What is the key length? (num or [a]ll): ').strip()
                if inp:
                    if inp[0] == 'a':
                        keylen = range(len(search_term), 24)
                    else:
                        keylen = [int(inp)]
            except ValueError:
                raise ValueError('not a number.')
        print()
        print('Available substition:')
        for _, _, pos, _, w in cur_words:
            for kl in keylen:
                res = SOLVER.substitute_get(pos, kl, search_term, w)
                print(f'{pos:04}: {res}')


#########################################
#                  G
#########################################

def command_g(cmd, args):  # (g)ematria primus
    if cmd not in 'gp gpr gpi':
        return False

    def pp(i):
        p, r, t = LP.alphabet[28 - i if rev else i]
        return '{:2d}  {} {:3d}  {}'.format(i, r, p, '/'.join(t))

    rev = cmd[-1] in 'ir' or len(args) > 0 and args[0] in 'ir'
    print('Gematria Primus (reversed)' if rev else 'Gematria Primus')
    half = (len(LP.alphabet) >> 1) + (len(LP.alphabet) & 1)  # ceil
    for i in range(half):
        if i < len(LP.alphabet) // 2:
            print('{:22} {}'.format(pp(i), pp(i + half)))
        else:
            print(pp(i))


#########################################
#                  H
#########################################

def command_h(cmd, args):  # (h)ighlight
    if cmd == 'h':
        SOLVER.reset_highlight()
        SOLVER.run()
    elif cmd in 'hj hi':
        res = SOLVER.highlight_interrupt()
        SOLVER.run()
        txt = ''
        bits = ''
        # first appearance of ᚠ is l_pos == 1; r_pos is the index on runes only
        for l_pos, r_pos, _, is_set in res:
            txt += '{}.{}.{}  '.format(l_pos, 'T' if is_set else 'F', r_pos)
            bits += '1' if is_set else '0'
        print(f'\nInterrupts: {bits}\n{txt}')
    else:
        return False


#########################################
#                  K
#########################################

def command_k(cmd, args):  # (k)ey manipulation
    if cmd == 'k' or cmd == 'key':
        SOLVER.KEY_DATA = LP.RuneText(args).index
        print(f'set key: {SOLVER.KEY_DATA}')
    elif cmd[1] == 's':
        SOLVER.KEY_SHIFT = get_cmd_int(cmd, args, 'shift')
    elif cmd[1] == 'r':
        SOLVER.KEY_ROTATE = get_cmd_int(cmd, args, 'rotation')
    elif cmd[1] == 'o':
        SOLVER.KEY_OFFSET = get_cmd_int(cmd, args, 'offset')
    elif cmd[1] == 'p':
        SOLVER.KEY_POST_PAD = get_cmd_int(cmd, args, 'post padding')
    elif cmd[1] == 'i':
        SOLVER.KEY_INVERT = not SOLVER.KEY_INVERT
        print(f'set key invert: {SOLVER.KEY_INVERT}')
    elif cmd == 'kj':
        args = args.strip('[]')
        pos = [int(x) for x in args.split(',')] if args else []
        SOLVER.INTERRUPT_POS = pos
        print(f'set interrupt jumps: {SOLVER.INTERRUPT_POS}')
    else:
        return False  # command not found
    SOLVER.run()


#########################################
#                  L
#########################################

def command_l(cmd, args):  # (l)og level
    if cmd == 'lv' or args == 'v' or args == 'verbose':
        SOLVER.output.VERBOSE = not SOLVER.output.VERBOSE
    elif cmd == 'lq' or args == 'q' or args == 'quiet':
        SOLVER.output.QUIET = not SOLVER.output.QUIET
    elif cmd == 'ln' or args == 'n' or args == 'normal':
        SOLVER.output.VERBOSE = False
        SOLVER.output.QUIET = False
    else:
        return False
    SOLVER.run()


#########################################
#                  P
#########################################

def command_p(cmd, args):  # (p)rime test
    if args and cmd not in 'prime':
        return False
    p = get_cmd_int(cmd, args, start=1)
    print(p, ':', LP.utils.is_prime(p))
    print(LP.utils.rev(p), ':', LP.utils.is_emirp(p))


#########################################
#                  T
#########################################

def command_t(cmd, args):  # (t)ranslate
    if cmd != 't':
        return False
    word = LP.RuneText(args)
    sffx = ''.join(['*' if LP.utils.is_prime(word.prime_sum) else '',
                    '√' if LP.utils.is_emirp(word.prime_sum) else ''])
    print('runes({}): {}'.format(len(word), word.rune))
    print('plain({}): {}'.format(len(word.text), word.text))
    print('reversed: {}'.format((~word).rune))
    print('indices: {}'.format(word.index))
    print('prime({}{}): {}'.format(word.prime_sum, sffx, word.prime))


#########################################
#                  X
#########################################

def command_x(cmd, args):  # e(x)ecute decryption
    if cmd == 'x':
        pass  # just run the solver
    elif cmd == 'xf':  # reload from file
        file = LP.path.page(args) if args else LP.path.root('_input.txt')
        print('loading file:', file)
        SOLVER.input.load(file=file)
        args = None  # so run() won't override data
    elif len(cmd) > 0 and cmd[1] == 'l':  # limit content
        limit = get_cmd_int(cmd, args, 'read limit')
        last_file = SOLVER.input.loaded_file
        if last_file:
            SOLVER.input.load(file=last_file)
        if limit > 0:
            SOLVER.input.data.trim(limit)
        args = None
    else:
        return False
    SOLVER.run(args if args else None)


if __name__ == '__main__':
    main()
