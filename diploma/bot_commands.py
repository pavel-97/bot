import help_user
import hello
import lowprice
import highprice
from typing import Dict

other_commands: Dict = {
    'Привет': hello.hello,
    r'/hello-world': hello.hello,
    r'/help': help_user.help_user,
}

commands: Dict = {
    r'/lowprice': lowprice.LowPrice,
    r'/highprice': highprice.HighPrice,
}

