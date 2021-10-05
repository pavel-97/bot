import help_user
import hello
import lowprice
from typing import Dict


commands: Dict = {
    'Привет': hello.hello,
    r'/hello-world': hello.hello,
    r'/help': help_user.help_user,
    r'/lowprice': lowprice.Lowprice,
}
