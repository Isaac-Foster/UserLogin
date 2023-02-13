from re import search

def cpf_validate(numbers) -> bool:
    cpf = [int(char) for char in numbers if char.isdigit()]
    if len(cpf) != 11:
        return False
    if cpf == cpf[::-1]:
        return False
    for i in range(9, 11):
        value = sum((cpf[num] * ((i + 1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        if digit != cpf[i]:
            return False
    return True


@dataclass
class Login:
    user: str
    passwd: str

    def __post_init__(self):
        try:
            valid = search(
                r'|'.join(
                    [
                        '(?P<cpf>^\d{3}.?\d{3}.?\d{3}.?\d{2}$)',
                        '(?P<email>^([a-zA-Z0-9\.]+)@([a-zA-Z0-9]+.\w+[.\w+]+?)$)',
                        '(?P<phone>^\+?[\ \d]{8,}$)',
                        '(?P<user>^[a-zA-Z0-9]+$)',
                    ]
                ),
                self.user,
            )

            valid_pass = search(
                '(?P<pin>^\d{4,8}$)|(?P<alf>^\w{5,}$)|(?P<other>^.{4,}$)',
                self.passwd,
            ).groupdict()
            type_user = {
                k: v for k, v in valid.groupdict().items() if v != None
            }
            type_pass = {kk: vv for kk, vv in valid_pass.items() if vv != None}

            if 'cpf' in type_user and cpf_validate(valid.group(0)):
                self.type_user = list(type_user)[0]
                self.user = valid.group(0)
            else:
                self.type_user = list(type_user)[0]
                self.user = valid.group(0)
            self.type_pass = list(type_pass)[0]
        except:
            raise ValueError()
