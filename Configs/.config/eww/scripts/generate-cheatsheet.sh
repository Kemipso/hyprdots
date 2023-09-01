#!/usr/bin/env sh

#rofiKeys=$(hyprkeys -c ~/.config/hypr/keybindings.conf -lbj -f rofi)
#windowKeys=$(hyprkeys -c ~/.config/hypr/keybindings.conf -lbj -f window)
#$HOME/gojq ".[] += [${windowKeys}]" test.json
hyprkeysJSON="hyprkeys -c $HOME/.config/hypr/keybindings.conf -lbj -f "
#testVar="hyprkeys -c $HOME/.config/hypr/keybindings.conf -lbj -f "
#echo $($testVar rofi)

echo '[[]]' > test.json

echo $($HOME/gojq ".[] += [$($hyprkeysJSON rofi)]" test.json) > test.json
echo $($HOME/gojq ".[][0] += {\"name\": \"rofi\"}" test.json) > test.json
$HOME/gojq . test.json
