# Unit 02 — 怎样完成并验证完整 Task Tracker？

> 状态：`BUILT` · 类型：BUILD / PROJECT<br>
> 起点：[06-object-model](../../06-classes-and-object-collaboration/03-compose-task-collaborators/06-object-model/)<br>
> 完整结果：[07-complete-task-tracker](07-complete-task-tracker/)

## 从验收反推最小修改

上一章已固定完整替换式编辑、稳定 ID 删除、状态筛选和输入结束策略。本章不重写一个新项目，而在对象版原有五个实现文件与入口上增量修改。旧四命令测试保留，避免新功能掩盖原功能退化。

先补模型与集合方法，再接 CLI，最后验证真实进程入口。若先堆命令分支，很容易把状态规则写进终端层，重新失去前几个 Module 建立的边界。

## 编辑：先得到可信值，再修改实例

错误思路是先 `self.title = title`，之后再判断优先级。失败时标题已经改变，用户却只看到“修改失败”。正式方法先得到全部可信值：

```python
def update(self, title, priority, note=None):
    title, priority, note = clean_fields(title, priority, note)
    self.title = title
    self.priority = priority
    self.note = note
```

clean_fields 失败时，没有任何已有属性被修改。成功时只更新三个可编辑字段，不碰 id 和 done。CLI 的 read_fields 同样先收集字段；模型仍重复保护约束，因为将来测试或其他调用者可能绕过 CLI。

TaskTracker.edit 先 find，调用 update 并返回同一个对象；不是新建 Task 替换，否则既有引用可能继续指向旧状态，也可能重置完成标记。

## 删除与筛选不能共用“删掉不想显示的记录”

删除找到目标后 `self._tasks.remove(task)`；下一 ID 计数器不回退。筛选则返回新列表：

```python
def select(self, status="all"):
    if status == "all":
        return self.all_tasks()
    if status == "pending":
        return [task for task in self._tasks if not task.done]
    if status == "done":
        return [task for task in self._tasks if task.done]
    raise ValueError("status must be all, pending, or done.")
```

这是 Module 03 comprehension 的自然落点：表达筛选后的集合值，而不是把副作用塞进表达式。返回顺序沿用原集合，元素仍是原 Task 对象。filter 结果 clear 不应影响正式成员，但修改某个 Task 仍是共享状态；测试准确区分这两点。

## 让界面适配参数，而不是侵入模型

`read_fields(read, editing=False)` 根据编辑场景改变标题和备注提示，返回相同三元组。editing 只描述界面文案，不传入 Task.update；模型不需要知道数据是从哪一种提示收来的。

路由使用 `case "list" | "list --pending" | "list --done":`，三个字面量共享展示分支。这里 `|` 表示备选模式，不是普通表达式中的布尔 or。匹配成功后才提取状态词，因此不对任意未知输入盲目 split。

edit 先确认 ID 存在，再读取新字段。若 ID 不存在，马上返回命令提示，不消耗随后本来打算输入的下一条命令。delete 同样只读取 ID。输入序列测试特别容易发现这类“多读了一行”的交互缺陷。

## 将退出策略放在会话外层

```python
def main(tracker=None, read=input, write=print):
    if tracker is None:
        tracker = TaskTracker()
    try:
        return run_cli(tracker, read, write)
    except EOFError:
        write("\nInput ended. Goodbye.")
        return 0
    except KeyboardInterrupt:
        write("\nCancelled. Goodbye.")
        return 130
```

main 的默认 tracker 用 None，不使用 `TaskTracker()` 作为默认表达式，防止定义时只创建一个实例并跨调用共享。__main__ 用 `raise SystemExit(main())` 将结果转成进程退出码。

EOF 或 Ctrl-C 不会被当成用户字段错误继续重试：输入已经结束，再反复读取只会形成无意义循环。与之相反，ValueError 属于当前命令失败，run_cli 显示后允许下一条命令。非预期 RuntimeError 仍向外传播，让缺陷可见。

## 交付验证不止“启动成功”

源码目录提供运行文档和三类行为测试。执行：

```bash
python3.14 -m task_tracker
python3.14 -m unittest discover -s tests -v
```

一组关键回归先创建两条任务，再完成第二条、筛选状态、编辑第一条、删除第二条、新增第三条。最后确认 #1 更新、#2 不再出现、#3 身份正确。

另一组直接在每个输入提示处注入 EOF，检查 add 没有追加、edit 没有部分更新。Ctrl-C 检查返回 130；真实子进程 EOF 检查退出 0、无 traceback；导入检查无输入输出。不能拿单元测试的 main 返回值代替所有入口证据。

测试没有覆盖任意对象类型、并发修改、持久化或所有操作系统的交互终端行为。当前字段 API 接收文档约定的类型；测试对业务无效值提供保护，而不是把任何对象都自动转换成任务。

## 练习：从一次失败定位责任

故意将 Task.update 中的标题赋值移到 clean_fields 之前，运行领域测试；然后恢复。再将 __main__ 中的 main 调用放在入口保护外，运行导入测试；最后恢复。记录失败的断言与责任层。

<details>
<summary>参考定位</summary>

第一项应由编辑失败保持原值的断言发现，原因是模型提交顺序，不是 CLI 文案。第二项应由安全导入测试发现，原因是入口副作用，不是业务规则。修复后重跑全套，防止只修到当前红色测试消失。

课程保留的是修复后的完整版本，故意改坏只发生在你的练习副本中，不修改先前教学里程碑。

</details>

Guided Build 到这里具备完整交付材料，但“照着正文做完”不等于独立迁移。下一 Unit 给出尚未讲过的需求；先提交自己的设计与证据，再看参考解。
