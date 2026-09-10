# 默认参数的对象生命周期

归属：[Unit 03](../)。只隔离“省略实参时是否创建新列表”，不是第三套 Task Tracker。

先预测两次调用是否共享对象，再运行 `python3.14 demo.py`。预期：

```text
shared default: True ['Read', 'Test']
fresh defaults: False ['Read'] ['Test']
explicit owner: ['Owned']
```

错误版默认列表随 def 建立而存在；修复版用 None 区分“未传入”与“传入空列表”。断言同时验证新建时隔离、显式传入时保留身份。故意错误被观察并断言，整个实验正常退出。
