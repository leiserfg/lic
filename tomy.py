import toml
import yaml
import sys




fields = ('title', 'nickname', 'category', 'source',
                 'required', 'permitted', 'forbidden')


def  purge(obj):
    clone = {}
    for f in fields:
        v = obj.get(f)
        clone[f] = v
    return clone


def translate(inp, out):
    inp = open(inp)
    out = open(out, mode='w')
    _, head, tail = inp.read().split('---')
    inp.close()
    obj = yaml.load(head)
    obj = purge(obj)

    out.write(toml.dumps(obj))
    out.write('\n---\n')
    tail = tail.replace('[', '{').replace(']', '}')
    out.write(tail)



if __name__ == '__main__':
   files = sys.argv[1:]
   for f in files:
        out = f.split('.')[:-1]

        out.append('lic')

        out = '.'.join(out)
        translate(f, out)

