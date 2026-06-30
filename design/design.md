# Game Arcade - 设计文档

## 概念
黑紫色霓虹主题迷你游戏平台，包含主界面、贪吃蛇和2048两款经典游戏。

## 页面路由
| 页面 | 文件 | 说明 |
|------|------|------|
| 主界面 | index.html | 游戏选择大厅，卡片式展示 |
| 贪吃蛇 | snake.html | 经典贪吃蛇，Canvas实现 |
| 2048 | 2048.html | 经典2048，DOM网格实现 |

## 配色系统
- 背景主色: `#050508` (极深黑)
- 背景次色: `#0a0612` (深紫黑)
- 卡片背景: `#11101a` / `#1a0a2e`
- 主紫色: `#9333ea` (violet-600)
- 亮紫色: `#a855f7` (violet-500)
- 霓虹紫: `#c084fc` (violet-400)
- 浅紫: `#d8b4fe` (violet-300)
- 文字主色: `#ffffff`
- 文字次色: `#a1a1aa` (zinc-400)
- 边框色: `#2e1065` (violet-950)
- 游戏网格: `#1a1a2e`

## 字体
- 标题: `Orbitron` (Google Fonts, 科幻风格)
- 正文: `Inter` (Google Fonts)
- 数字/分数: `Orbitron`

## 布局规则
- 最大宽度: 1200px
- 移动端: 100% 宽度，padding 16px
- 游戏画布: 贪吃蛇 400x400, 2048 4x4 网格 360px
- 卡片圆角: 16px
- 按钮圆角: 12px

## 交互语言
- 按钮 hover: 紫色渐变发光，scale 1.02
- 卡片 hover: 紫色边框发光，上浮 4px
- 过渡: all 0.3s ease
- 粒子背景效果 (Canvas)
- 霓虹文字发光: text-shadow

## 共享组件
- 顶部导航栏: Logo + 返回按钮
- 页脚: 版权信息
- 粒子背景 Canvas
- 紫色渐变按钮

## 依赖
- Google Fonts: Orbitron, Inter
- 纯原生 JS，无框架
