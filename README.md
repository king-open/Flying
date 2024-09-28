# 热补丁系统

> 一个用于动态修复运行中Python代码的热补丁系统。

## 功能特点

- 动态修复运行中的Python代码
- 自动监控服务并应用补丁
- 线程安全的补丁应用机制

## 快速开始

1. 克隆仓库：

   ```bash
   
  git clone git@github.com:king-open/Flying.git 

  cd Flying
   ```

2. 运行系统：
   ```
   python hot_patching_system.py
   ```

## 核心组件

- `HotPatcher`: 热补丁核心类，负责应用和恢复补丁
- `BuggyService`: 模拟有bug的服务类
- `monitor_and_patch`: 监控服务并应用补丁的函数

## 使用示例

```python

hot_patcher = HotPatcher()
service = BuggyService()

```
### 应用补丁 

```python
hot_patcher.apply_patch(BuggyService, "process", fixed_process)

```

### 恢复补丁

```python
hot_patcher.revert_patch(BuggyService, "process")
```


## 注意事项

- 本系统主要用于演示和学习目的
- 在生产环境中使用时，请确保进行充分的测试和安全评估


## 许可证

[MIT](https://choosealicense.com/licenses/mit/)
