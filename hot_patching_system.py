import types
import threading
import time
import traceback

class HotPatcher:
    """
    热补丁系统的核心类，用于动态修改类的方法。
    """
    def __init__(self):
        self.lock = threading.Lock()  # 用于确保线程安全
        self.patched_classes = {}  # 存储被修补的类和方法

    def apply_patch(self, target_class, method_name, new_method):
        """
        应用补丁到指定类的方法。
        
        :param target_class: 目标类
        :param method_name: 要修补的方法名
        :param new_method: 新的方法实现
        """
        with self.lock:
            if target_class not in self.patched_classes:
                self.patched_classes[target_class] = {}
            
            # 保存原始方法以便之后可以恢复
            if method_name not in self.patched_classes[target_class]:
                self.patched_classes[target_class][method_name] = getattr(target_class, method_name)
            
            # 应用新方法
            setattr(target_class, method_name, types.MethodType(new_method, target_class))
            print(f"Applied patch: {target_class.__name__}.{method_name}")

    def revert_patch(self, target_class, method_name):
        """
        恢复指定类的方法到原始实现。
        
        :param target_class: 目标类
        :param method_name: 要恢复的方法名
        """
        with self.lock:
            if target_class in self.patched_classes and method_name in self.patched_classes[target_class]:
                original_method = self.patched_classes[target_class][method_name]
                setattr(target_class, method_name, original_method)
                del self.patched_classes[target_class][method_name]
                print(f"Reverted patch: {target_class.__name__}.{method_name}")

class BuggyService:
    """
    模拟一个有bug的服务类。
    """
    def __init__(self):
        self.running = True
        self.counter = 0

    def process(self, data):
        """
        处理数据的方法，每5次调用会抛出一个异常。
        
        :param data: 要处理的数据
        :return: 处理后的数据
        :raises ValueError: 当 counter 是5的倍数时
        """
        self.counter += 1
        if self.counter % 5 == 0:
            raise ValueError("Simulated bug: can't process data divisible by 5")
        return f"Processed: {data}"

    def run(self):
        """
        运行服务的主循环。
        """
        while self.running:
            try:
                data = f"data_{self.counter}"
                result = self.process(data)
                print(result)
            except Exception as e:
                print(f"Error: {str(e)}")
                traceback.print_exc()
            time.sleep(1)

def monitor_and_patch(service, hot_patcher):
    """
    监控服务并在检测到多次错误时应用补丁。
    
    :param service: 要监控的服务实例
    :param hot_patcher: HotPatcher实例
    """
    error_count = 0
    while service.running:
        if error_count >= 3:
            print("Detected multiple errors. Applying hot patch...")
            def fixed_process(self, data):
                """
                修复后的process方法，移除了导致异常的代码。
                """
                self.counter += 1
                return f"Fixed Process: {data}"
            
            hot_patcher.apply_patch(BuggyService, "process", fixed_process)
            break
        time.sleep(1)
        if service.counter % 5 == 0:
            error_count += 1

def main():
    """
    主函数，设置并运行整个系统。
    """
    hot_patcher = HotPatcher()
    service = BuggyService()

    # 启动服务线程
    service_thread = threading.Thread(target=service.run)
    service_thread.start()

    # 启动监控线程
    monitor_thread = threading.Thread(target=monitor_and_patch, args=(service, hot_patcher))
    monitor_thread.start()

    try:
        time.sleep(30)  # 运行30秒
    finally:
        service.running = False
        service_thread.join()
        monitor_thread.join()

if __name__ == "__main__":
    main()
