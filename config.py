import subprocess
import os
import functools

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

mod = "mod4"
terminal = guess_terminal()

keys = [
    # Applications
    Key([mod, "shift"], "Return", lazy.spawn("thunar"), desc="File manager"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Terminal" ),
    Key([mod, "shift"], "s", lazy.spawn("flameshot gui"), desc="Screenshot tool"),
    Key([mod], "d", lazy.spawn("rofi -show drun"), desc="App launcher"),
    Key([mod], "tab", lazy.spawn("rofi -show window"), desc="Show open apps"),
    Key([mod], "l", lazy.spawn("betterlockscreen -l"), desc="Simple lockscreen"),

    # Multimedia keys 
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +5%"), desc="Raise brightness level by 5%"),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5-%"), desc="Lower brightness level by 5%"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer sset Master 5%+"), desc="Raise volume level by 5%"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer sset Master 5%-"), desc="Lower volume level by 5%"),
    Key([], "XF86AudioMute", lazy.spawn("amixer sset Master 1+ toggle"), desc="Mute or unmute volume level"),

    # Window control using arrow keys
    # Change window focus
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    # Move focused window
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),
    # Resize Windows
    Key([mod, "control"], "Right", lazy.layout.grow_right(), lazy.layout.grow(), lazy.layout.increase_ratio(), lazy.layout.delete()),
    Key([mod, "control"], "Left", lazy.layout.grow_left(), lazy.layout.shrink(), lazy.layout.decrease_ratio(), lazy.layout.add()),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), lazy.layout.grow(), lazy.layout.decrease_nmaster()),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), lazy.layout.shrink(), lazy.layout.increase_nmaster()),

    # Toggle between different layouts as defined below
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen on the focused window"),
    Key([mod], "space", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
]

groups = [Group(i) for i in "12345678"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key([mod], i.name, lazy.group[i.name].toscreen(), desc="Switch to group {}".format(i.name)),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True), desc="Switch to & move focused window to group {}".format(i.name)),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

one_dark = {
    "background": "282c34", #1e2127
    "foreground": "abb2bf",
    "black":      "5c6370",
    "red":        "e06c75",
    "green":      "98c379",
    "yellow":     "d19a66",
    "blue":       "61afef",
    "magenta":    "c678dd",
    "cyan":       "56b6c2",
    "white":      "828791",
    "accent":     "61afef"
}

theme = one_dark
accent_color = theme["accent"]

layout_defaults = {
    "border_width": 2,
    "border_focus": "#000000",
    "border_normal": theme["black"]
}

layouts = [
    layout.MonadTall(border_focus="#61afef", border_normal="#5c6370", border_width=2, margin=5),
    layout.Max()
]

widget_defaults = dict(
    font="Cantarell",
    fontsize=14,
    padding=6,
)
extension_defaults = widget_defaults.copy()

# Presets for icons and seperator
icon = lambda char, foreground, background: widget.TextBox(
    font="Font Awesome 6 Free Solid",
    text=char,
    background=background,
    foreground=foreground,
)

separator = lambda color: widget.Sep(
    background=color,
    foreground=color,
)

separator_background_color = functools.partial(separator, color=theme["background"])

screens = [
    Screen(
        top=bar.Bar(
            [
                separator(color=theme["background"]),
                widget.GroupBox(
                    font="Cantarell",
                    highlight_method="text",
                    this_current_screen_border=accent_color,
                    inactive=theme["black"],
                    borderwidth=0,
                    padding_x=8,
                    padding_y=8,
                    margin_x=0
                ),
                # separator(color=theme["background"]),
                widget.WindowName(
                    font="Cantarell",
                    fontsize=14,
                    foreground=theme["yellow"]
                ),
                # separator(color=theme["background"]),
                icon("\uf1eb", background=theme["background"], foreground=theme["accent"]),
                widget.Net(
                    format="{down} ↓↑{up}",
                    prefix="M",
                    foreground=theme["yellow"],
                ),
                # separator(color=theme["background"]),
                icon("\uf2db", background=theme["background"], foreground=theme["accent"]),
                widget.Memory(
                    measure_mem="G",
                    format="{MemUsed:.1f}/{MemTotal:.1f} GiB",
                    background=theme["background"],
                    foreground=theme["yellow"]
                ),
                # separator(color=theme["background"]),
                icon("\uf2db", background=theme["background"], foreground=theme["accent"]),
                widget.CPU(
                    format="{load_percent:.1f}%",
                    background=theme["background"],
                    foreground=theme["yellow"]
                ),
                # separator(color=theme["background"]),
                icon("\uf0eb", background=theme["background"], foreground=theme["accent"]),
                widget.Backlight(
                    backlight_name = 'intel_backlight',
                    fmt = '{}',
                    background=theme["background"],
                    foreground=theme["yellow"]
                ),
                # separator(color=theme["background"]),
                icon("\uf028", background=theme["background"], foreground=theme["accent"]),
                widget.Volume(
                    fmt = '{}',
                    background=theme["background"],
                    foreground=theme["yellow"]
                ),
                # separator(color=theme["background"]),
                icon("\uf240", background=theme["background"], foreground=theme["accent"]),
                widget.Battery(
                    format = "{percent:2.0%}",
                    background=theme["background"],
                    foreground=theme["yellow"]
                ),
                # separator(color=theme["background"]),
                icon("\uf073", background=theme["background"], foreground=theme["accent"]),
                widget.Clock(
                    format="%b %d, %Y",
                    background=theme["background"],
                    foreground=theme["yellow"],
                ),
                # separator(color=theme["background"]),
                icon("\uf017", background=theme["background"], foreground=theme["accent"]),
                widget.Clock(
                    format="%I:%M %p",
                    background=theme["background"],
                    foreground=theme["yellow"],
                ),
                # separator(color=theme["background"]),
                widget.Systray(
                    fontsize=12,
                    background=theme["background"],
                ),
                separator(color=theme["background"]),
            ],
            28,
            background=theme["background"],
            border_color=["#61afef", "#61afef", "#61afef", "#61afef"],
            border_width=[2, 2, 2, 2],
            margin=[5, 5, 0, 5],
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    border_width=2,
    border_focus="#61afef",
    border_normal="#5c6370",
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~/.config/qtile/scripts/autostart.sh')
    subprocess.call([home])
