from better_launch import BetterLaunch, launch_this


@launch_this
def first_steps():
    bl = BetterLaunch()

    with bl.group("basic"):
        bl.node(
            "my_first_package",
            "talker",
            "my_talker",
        )
        bl.node(
            "my_first_package",
            "listener",
            "my_listener",
        )

