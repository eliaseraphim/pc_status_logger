from pathlib import Path
import shutil
import psutil


def percentage_bar(prefix, percentage, suffix=None, indent=''):
    if type(percentage) not in (int, float):
        raise Exception(f'Invalid Types: percentage must be int or float. type(percentage): {type(percentage)}')

    text = f'{indent}{prefix} | ['
    for percentage_block in range(0, 100, 5):
        if percentage_block < percentage:
            text += '█'
        else:
            text += '-'
    if suffix is not None:
        text += f'] {percentage:>5.1f}% | {suffix}\n'
    else:
        text += f'] {percentage:>5.1f}%\n'

    return text


def memory_default(memory, indent):
    text = ''

    # total memory
    total_KiB = memory.total / 1024
    total_MiB = total_KiB / 1024
    total_GiB = total_MiB / 1024

    # used memory
    # total memory
    used_KiB = memory.used / 1024
    used_MiB = used_KiB / 1024
    used_GiB = used_MiB / 1024

    # free memory
    free_KiB = memory.free / 1024
    free_MiB = free_KiB / 1024
    free_GiB = free_MiB / 1024

    # ratio
    percent_used = (memory.used / memory.total) * 100
    percent_free = (memory.free / memory.total) * 100

    text += percentage_bar(  # used storage
        f'% Used',
        percent_used,
        suffix=(
                f'{f"{used_KiB:.2f}" + " KiB":<18}| ' +
                f'{f"{used_MiB:.2f}" + " MiB":<15}| ' +
                f'{f"{used_GiB:.2f}" + " GiB":<12}'
        ),
        indent=f'{indent * 2}'
    )
    text += percentage_bar(  # free storage
        f'% Free',
        percent_free,
        suffix=(
                f'{f"{free_KiB:.2f}" + " KiB":<18}| ' +
                f'{f"{free_MiB:.2f}" + " MiB":<15}| ' +
                f'{f"{free_GiB:.2f}" + " GiB":<12}'
        ),
        indent=f'{indent * 2}'
    )
    text += (  # total storage
            f'\t\tTotal Space | ' +
            f'{total_KiB:.2f} KiB | ' +
            f'{total_MiB:.2f} MiB | ' +
            f'{total_GiB:.2f} GiB\n'
    )

    return text


def cpu_status(indent='\t', verbose=False):
    # number of cpus (physical)
    def physical_cpus():
        text = f'{indent}Physical CPUS | {psutil.cpu_count(logical=False)} \n'

        if verbose:
            print(text)
        return text + '\n'

    # number of cpus (logical)
    def logical_cpus():
        text = f'{indent}Logical CPUS | {psutil.cpu_count(logical=True)} \n'

        if verbose:
            print(text)
        return text + '\n'

    # cpu frequency
    def cpu_frequency():
        cpu_freq = psutil.cpu_freq()
        text = (
                f'{indent}CPU Frequency \n' +
                f'{indent * 2}Current | {cpu_freq.current / 1000:.2f} GHz \n' +
                f'{indent * 2}Minimum | {cpu_freq.min / 1000:.2f} GHz \n' +
                f'{indent * 2}Maximum | {cpu_freq.max / 1000:.2f} GHz \n'
        )
        if verbose:
            print(text)

        return text + '\n'

    # cpu times (overall)
    def cpu_times():
        cpu_times_overall = psutil.cpu_times(percpu=False)
        cpu_times_per_cpu = psutil.cpu_times(percpu=True)
        text = (
            f'{indent}CPU Times | Overall [Since Boot] \n' +
            f'{indent * 2}User   | {cpu_times_overall.user:.2f} seconds \n' +
            f'{indent * 2}System | {cpu_times_overall.system:.2f} seconds \n' +
            f'{indent * 2}Idle   | {cpu_times_overall.idle:.2f} seconds \n\n' +
            f'{indent}CPU Times | Per Logical CPU [Since Boot]\n'
        )

        for index, times in enumerate(cpu_times_per_cpu):
            text += (
                f'{indent * 2}CPU | {index} \n' +
                f'{indent * 3}User   | {times.user:.2f} seconds \n' +
                f'{indent * 3}System | {times.system:.2f} seconds \n' +
                f'{indent * 3}Idle   | {times.idle:.2f} seconds \n'
            )
            if index + 1 != len(cpu_times_per_cpu):
                text += '\n'
        if verbose:
            print(text)

        return text + '\n'

    def cpu_utilization():
        text = f'{indent}CPU Utilization\n'
        if verbose:
            print(text, end='')

        for index in range(10):
            temp_text = percentage_bar(
                f'Trial: {index}',
                psutil.cpu_percent(interval=1),
                suffix='Time: 1 Second',
                indent=f'{indent * 2}'
            )
            if verbose:
                if index < 9:
                    print(temp_text, end='')
                else:
                    print(temp_text)
            text += temp_text

        return text + '\n'

    full_text = 'CPU Status'
    if verbose:
        print(full_text)

    full_text += physical_cpus()
    full_text += logical_cpus()
    full_text += cpu_frequency()
    full_text += cpu_times()
    full_text += cpu_utilization()

    return full_text + '\n'


def memory_status(indent='\t', verbose=False):
    # virtual memory statistics
    def virtual_memory():
        vm = psutil.virtual_memory()
        text = f'{indent}Virtual Memory\n' + memory_default(vm, indent)

        if verbose:
            print(text)
        return text + '\n'

    # swap memory statistics
    def swap_memory():
        sm = psutil.swap_memory()
        text = f'{indent}Swap Memory\n' + memory_default(sm, indent)

        if verbose:
            print(text)
        return text + '\n'

    full_text = 'System Memory'
    if verbose:
        print(full_text)

    full_text += virtual_memory()
    full_text += swap_memory()

    return full_text + '\n'


def disk_usage(disk, indent='\t', verbose=False):
    du = shutil.disk_usage(disk)
    text = f'Disk Usage\n{indent}Current Disk: {disk}\n' + memory_default(du, indent)

    if verbose:
        print(text)
    return text + '\n'


def network_status():
    # network io statistics
    # network connections
    # network card information
    # network card statistics
    pass


def sensors_status():
    # sensors temperature
    # fan information
    # battery information
    pass


def boot_status():
    pass


def users_status():
    pass


def processes_status():
    # current number of processes
    # process information
    pass


def check_nvidia_gpu():
    # may need to use a different tool
    pass


def main():
    text = cpu_status(indent='  ', verbose=True)
    text += memory_status(indent='  ', verbose=True)
    text += disk_usage('C:', indent='  ', verbose=True)
    text += disk_usage('D:', indent='  ', verbose=True)


if __name__ == '__main__':
    main()
