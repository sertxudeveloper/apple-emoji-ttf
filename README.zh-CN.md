![AppleColorEmoji-ttf](https://repository-images.githubusercontent.com/158348890/3d33a645-a079-4150-860a-8cea647732b2)

语言：[English](README.md) | 简体中文

# apple-emoji-ttf

在 Linux、Windows 和网页中使用 Apple Color Emoji。

本仓库提供转换脚本、构建配置和发行包。由于版权原因，仓库里不包含 Apple 原始字体。自行构建时请从 macOS 获取 `Apple Color Emoji.ttc`。

## 说明

本项目仅供学习和研究使用。Apple Color Emoji 的字体资源和设计归 Apple Inc. 所有。Apple 是 Apple Inc. 在美国及其他国家和地区的注册商标。

跨系统或在网页中使用该字体可能涉及授权问题，请自行确认使用范围。

## 下载

不想自己构建的话，直接到 [Releases](https://github.com/samuelngs/apple-emoji-ttf/releases) 下载对应平台的文件：

- Ubuntu / Debian 用 `fonts-apple-color-emoji.deb`
- Fedora / RHEL 用 `fonts-apple-color-emoji.rpm`
- Arch Linux 用 `ttf-apple-emoji.pkg.tar.zst`
- Linux 手动安装用 `AppleColorEmoji-Linux.ttf`
- Windows 用 `AppleColorEmoji-Windows.ttf`
- Web 用法见下面的“Web”部分

## Linux

Ubuntu / Debian：

```bash
sudo dpkg -i fonts-apple-color-emoji.deb
# 或
sudo apt install ./fonts-apple-color-emoji.deb
```

Fedora / RHEL：

```bash
sudo dnf install ./fonts-apple-color-emoji.rpm
# 或
sudo rpm -i fonts-apple-color-emoji.rpm
```

Arch Linux：

```bash
sudo pacman -U ttf-apple-emoji.pkg.tar.zst
```

手动安装：

```bash
mkdir -p ~/.local/share/fonts
cp AppleColorEmoji-Linux.ttf ~/.local/share/fonts/
```

装好字体后，系统不一定会马上拿它显示 Emoji。很多桌面应用实际听 fontconfig 的排序。

先在 `/etc/fonts/conf.d/60-generic.conf`（或发行版对应文件）里找到 `<family>emoji</family>` 的 `<alias>`，把 Apple Color Emoji 放到 `<prefer>` 最前面：

```xml
<family>Apple Color Emoji</family>
```

再创建或更新 `~/.config/fontconfig/fonts.conf`。可以直接使用仓库里的 `fonts.conf`，让 serif、sans-serif、monospace 和 Noto Color Emoji 的请求优先走 Apple Color Emoji。

最后刷新缓存：

```bash
fc-cache -fv
```

## Windows

Windows 版本是一个普通的字体文件，家族名就是 `Apple Color Emoji`。它不会修改、替换或重命名系统的 `Segoe UI Emoji`。

从 [Releases](https://github.com/samuelngs/apple-emoji-ttf/releases) 下载 `AppleColorEmoji-Windows.ttf`，然后右键点击选择**安装**；如果希望所有用户都能用，就选**为所有用户安装**。也可以直接把文件放进 `%LOCALAPPDATA%\Microsoft\Windows\Fonts`（当前用户）或 `C:\Windows\Fonts`（所有用户）。

卸载：打开**设置 → 个性化 → 字体**，选中 `Apple Color Emoji`，点**卸载**。

**应用如何用上它：** Windows 自己会把 Emoji 交给 Segoe UI Emoji 渲染，这个回退位置是字体无法占用的。所以光装上不会改变屏幕上任何 Emoji，必须在具体应用里指定 `Apple Color Emoji`。常见做法：

- **Chrome / Edge 等 Chromium 浏览器** - 用用户样式表或 `@font-face` 规则，把 `src` 指向 `.ttf`，并用 `unicode-range` 限定只覆盖 Emoji，这样其他字符仍然走原来的字体：

  ```css
  @font-face {
    font-family: "Apple Color Emoji";
    src: url("file:///C:/Windows/Fonts/AppleColorEmoji-Windows.ttf") format("truetype");
    unicode-range: U+1F000-1FAFF, U+2600-27BF, U+2B00-2BFF, U+FE0F, U+200D, U+1F1E6-1F1FF;
  }
  body { font-family: "Apple Color Emoji", system-ui, sans-serif; }
  ```

- **VS Code 等 Electron 应用** - 把对应设置项写成 `"Apple Color Emoji", <你原来的字体>`，例如 `settings.json` 里的 `"editor.fontFamily"`。
- **其他应用** - 只要应用提供字体选择器，就直接选 `Apple Color Emoji`。

如果你想让 Emoji 全局替换 Segoe UI Emoji，这个字体做不到。`C:\Windows\Fonts\seguiemj.ttf` 受 Windows 资源保护（WRP）保护，在 Windows 11 上只能离线修改系统镜像才能替换，这会导致 Windows 更新失败，也可能让系统无法启动。

## Web

Web 版本建议用 `configs/web.yaml` 单独构建。它不会只输出一个大字体文件，而是顺手生成 CSS，并把字体拆成多个分片，浏览器用到哪个 Emoji 再加载对应文件。

先构建：

```bash
python cli.py -c configs/web.yaml --output output/AppleColorEmoji.ttf
```

输出目录大概会长这样：

```text
output/
  AppleColorEmoji.css
  AppleColorEmoji[1].ttf
  AppleColorEmoji[2].ttf
  ...
```

部署时把这些文件放在同一个目录下，页面里引入 CSS：

```html
<link rel="stylesheet" href="/fonts/AppleColorEmoji.css">
```

然后在需要显示 Apple Emoji 的地方指定字体：

```css
.emoji {
  font-family: "Apple Color Emoji", system-ui, sans-serif;
}
```

如果你改了目录结构，记得同步改 `AppleColorEmoji.css` 里的 `src:` 路径。

## 自行构建

依赖：

- Python 3.12+
- `pip install -r requirements.txt`
- `Apple Color Emoji.ttc`

macOS 默认字体路径：

```text
/System/Library/Fonts/Apple Color Emoji.ttc
```

如果就在 macOS 上跑脚本，可以省掉 `--input`：

```bash
pip install -r requirements.txt
python cli.py -c configs/linux.yaml --output output/AppleColorEmoji-Linux.ttf
python cli.py -c configs/windows.yaml --output output/AppleColorEmoji-Windows.ttf
python cli.py -c configs/web.yaml --output output/AppleColorEmoji.ttf
```

如果字体文件在其他位置：

```bash
python cli.py -c configs/linux.yaml --input "/path/to/Apple Color Emoji.ttc" --output output/AppleColorEmoji-Linux.ttf
```

不同平台使用不同配置：

- `configs/linux.yaml`
- `configs/windows.yaml`
- `configs/web.yaml`

### 更新 Emoji 序列

```bash
python tools/update_emoji_data.py --version latest
# 或指定版本
python tools/update_emoji_data.py --version 17.0
```

也可以在构建前更新：

```bash
python cli.py -c configs/web.yaml --output output/AppleColorEmoji.ttf --update-sequences
python cli.py -c configs/windows.yaml --output output/AppleColorEmoji-Windows.ttf --update-sequences 17.0
```

`sequences/project-sequences.txt` 是项目维护的补充数据，不会从 Unicode 下载。

## 已知问题

- 部分 Linux 应用里的 Emoji 可能偏小。
- 部分 Qt 应用可能无法正确显示彩色 Emoji。
- Windows 会自行把 Emoji 交给 Segoe UI Emoji 渲染，这个回退位置改不了，所以 Windows 版本是作为独立字体安装的，需要在应用里手动指定 `Apple Color Emoji`（见上面的 Windows 部分）。

## 许可证

代码部分采用 [MIT License](LICENSE)。Apple Color Emoji 本身仍归 Apple 所有。
