# 作用域与重新绑定

归属：[Unit 03](../)。运行 `python3.14 demo.py`，预期：

```text
rebinding before local value: UnboundLocalError
caller: ['visible']
returned: ['local']
```

先预测 counter 是否会变成 1。局部赋值使读取面向尚未绑定的局部名字，因此错误被准确捕获，模块 counter 保持 0。第二组固定同一个列表参数，只改变操作：append 对调用者可见，重新赋值只影响局部名字。实验不使用 global 修补，以免隐藏显式数据流的替代方案。
