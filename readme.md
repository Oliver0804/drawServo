
# QT 視覺化機械手臂控制

這個專案提供了一個QT應用程式，用於控制和視覺化XY平面上的兩節機械手臂的角度和動作。這個GUI展示了使用者與滑塊互動時機械手臂的實時位置，並根據逆向運動學公式計算角度。此外，計算出的伺服角度會被映射到適當的PWM值，以供搭配Arduino控制的伺服器使用。

## 代碼示例

```bash
python main.py
```
需確認已經安裝pyqt5

## 展示

您可以在下面看到應用程式的展示：

![展示](https://github.com/Oliver0804/drawServo/blob/main/demo.gif)

