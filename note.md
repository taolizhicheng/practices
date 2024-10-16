更新内容
===
feat
---
1. metric新增__str__和__repr__方法
2. model新增backbone目录，新增resnet结构
3. postprocessor新增__str__和__repr__方法
4. scheduler新增__str__和__repr__方法
5. build新增参数类型检查
6. 新增本地安装和卸载脚本
7. 新增note文件，用于记录更新内容
8. 新增chatdet依赖
---
fix
---
1. base dataset的__getitem__方法返回格式错误
2. ast修复相对路径获取问题