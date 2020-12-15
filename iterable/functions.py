class Function:
    @staticmethod
    def gnome_sort(initial_list, function):
        index = 0
        list = initial_list[:]
        length = len(list)
        while index < length:
            if index == 0:
                index += 1
            elif function(list[index - 1], list[index]) == True:
                index += 1
            else:
                list[index], list[index-1] = list[index-1], list[index]
                index -= 1
        return list

    @staticmethod
    def filter(list, criteria, parameter=None):
        filtered_list = []
        for index in range(len(list)):
            if criteria(list[index], parameter) == True:
                filtered_list.append(list[index])
        return filtered_list[:]