import datetime
import time


class Utils:
    @staticmethod
    def decorator_timer_name(arg_decorator:str=None):
        def decorator(func):
            def wrapper(*args, **kwargs):
                start_time = datetime.datetime.now()
                result = func(*args, **kwargs)
                print ("Я - обёртка вокруг декорируемой функции.\n")
                #       "И я имею доступ ко всем аргументам: \n"
                #       "\t- и декоратора: {0} \n"
                #       "\t- и функции: {1} {2} \n"
                #       "Теперь я могу передать нужные аргументы дальше"
                #       .format(args_decorator,
                #               function_arg1, function_arg2))   
                end_time = datetime.datetime.now()
                elapsed_time = end_time - start_time
                
                if arg_decorator:
                    print(f"Время выполнения {arg_decorator}: {elapsed_time}")
                else:
                    print(f"Время выполнения {func.__name__}: {elapsed_time}")
                return result

            return wrapper
        return decorator

    @staticmethod
    def decorator_timer(func):
            def wrapper(*args, **kwargs):
                start_time = datetime.datetime.now()
                result = func(*args, **kwargs)

                end_time = datetime.datetime.now()
                elapsed_time = end_time - start_time

                print(f"Время выполнения {func.__name__}: {elapsed_time}")
                return result

            return wrapper

