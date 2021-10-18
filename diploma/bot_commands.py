import help_user
import hello
import lowprice
import highprice
import bestdeal
import history
from typing import Dict

other_commands: Dict = {
    'Привет': hello.hello,
    r'/hello-world': hello.hello,
    r'/help': help_user.help_user,
    r'/history': history.history,
}

commands: Dict = {
    r'/lowprice': lowprice.LowPrice,
    r'/highprice': highprice.HighPrice,
    r'/bestdeal': bestdeal.BestDeal,
}
