def find_methods_and_args(p_children, f_lines):
    import re
    funcRE = re.compile(r'(.*)@(.*)')

    def break_s(node, lines):
        ret = []
        latest_pos = []
        for outer in node.split('<'):
            if outer.startswith('Name: '):
                inner = outer.split('>')
                for one in inner:
                    if one.startswith('Name: '):
                        one_broken = one[6:].split('@')
                        pos = one_broken[1].split(',')
                        latest_pos = [int(pos[0]), int(pos[1])]
                        ret.append([one_broken[0], pos[0], pos[1]])
            elif outer.startswith('Operator: '):
                inner = outer.split('>')
                for one in inner:
                    if one.startswith('Operator: '):
                        one_broken = one[10:]
                        ret.append(one_broken)
            elif outer.startswith('Number: ') or outer.startswith('String: '):
                if latest_pos == []:
                    find = re.search(r'@(\d+,\d+)>', node).group(1).split(',')
                    latest_pos = [int(find[0]), int(find[1])]
                inner = outer.split('>')
                for one in inner:
                    if one.startswith('Number: ') or one.startswith('String: '):
                        one_broken = one[8:]
                        one_broken.replace('\r\n', '\n')
                        one_broken = one_broken.split('\n')
                        one_broken = one_broken[-1]
                        found_pos = False
                        pos = []
                        i = 0
                        first = True
                        starts_w_string = False
                        if node[2:].startswith('String'):
                            starts_w_string = True
                        while not found_pos:
                            if first:
                                #try:
                                result = lines[latest_pos[0]-1+i][latest_pos[1]:].find(one_broken)
                                if starts_w_string:
                                    i -= 1
                                #except IndexError:
                                #    print('||||||||||')
                                #    print(latest_pos)
                                #    print(lines[latest_pos[0]-1+i])
                                #    print(lines[latest_pos[0]-1+i][latest_pos[1]:])
                                #    print(one_broken)
                            else:
                                try:
                                    #print(one_broken)
                                    result = lines[latest_pos[0]-1+i].find(one_broken)
                                except IndexError:
                                    if lines[latest_pos[0]-1].find(one_broken) != -1:
                                        # not a function
                                        return []
                                    raise IndexError
                                    # # print(node)
                                    # # print('|||||||||')
                                    # print(lines[latest_pos[0] - 1][latest_pos[1]:])
                                    # print(one_broken)
                                    # print(latest_pos)
                                    # print(i)
                                    # # print(one_broken)
                                    # print(latest_pos[0]-1)
                                    # # print(lines[latest_pos[0]-1+i])
                                    # exit()
                            if result == -1:
                                i += 1
                                first = False
                                continue
                            else:
                                found_pos = True
                                if first:
                                    pos = [latest_pos[0]+i, latest_pos[1] + result]
                                else:
                                    pos = [latest_pos[0]+i, result]
                        ret.append([one_broken, pos[0], pos[1]])
        return ret

    def get_params(l):
        params = []
        for one in l:
            one = str(one)[15:].rstrip('>>')
            l_one = one.split('@')
            pos = l_one[1].split(',')
            params.append([l_one[0], pos[0], pos[1]])
        return params

    # methods format: [start line, end line, starting offsets in all lines for function, ending offsets same way]
    # parameters format: [line, starting offset, ending offset]
    methods = []
    parameters = []

    def get_methods_and_args(children, lines):
        for one in children:
            if (str(type(one)).split('.')[-1][:-2] == 'PythonNode' and one.type == 'atom_expr') or \
               one.type == 'funcdef':
                node = str(one).lstrip('PythonNode(atom_expr, ').rstrip(')')
                if one.type == 'funcdef':
                    params = get_params(one.get_params())
                    func = funcRE.search(node)
                    pos = func.group(2).split('-')
                    methods.append([int(pos[0])-1,
                                    int(pos[1][:-1])-2,
                                    [len(k)-len(k.strip())-1 for k in lines[int(pos[0])-1:int(pos[1][:-1])-1]],
                                    [len(k) for k in lines[int(pos[0])-1:int(pos[1][:-1])-1]]])
                    for param in params:
                        for ip, p_content in enumerate(param[1:]):
                            if re.fullmatch(r'\d+', p_content) is None:
                                try:
                                    param[ip+1] = re.fullmatch(r'(\d+).*', p_content).group(1)
                                except AttributeError:
                                    break
                        try:
                            parameters.append([int(param[1]) - 1, int(param[2]), int(param[2]) + len(param[0]) - 1])
                        except ValueError:
                            continue
                else:
                    #print(node)
                    try:
                        broken_nodes = break_s(node, lines)
                    except IndexError:
                        continue
                    #print(broken_nodes)
                    if not broken_nodes:
                        continue
                    # except IndexError:
                    #     print(one)
                    #     exit()
                    #print(broken_nodes)
                    level = 0
                    while 1:
                        if broken_nodes[0] == '(':
                            broken_nodes = broken_nodes[1:]
                        else:
                            break
                    for i, each_node in enumerate(broken_nodes):
                        if each_node == '(':
                            level += 1
                            num_ls = 1
                            num_rs = 0
                            start_back_search = None
                            for j, find in enumerate(broken_nodes[i+1:]):
                                if find == '(':
                                    num_ls += 1
                                elif find == ')':
                                    num_rs += 1
                                if num_ls == num_rs:
                                    start_back_search = i + j
                                    break
                            while 1:
                                if isinstance(broken_nodes[start_back_search], list):
                                    # try:
                                    z = 0
                                    start_l_failure = False
                                    while 1:
                                        try:
                                            start_l = int(broken_nodes[i-(1+z)][1]) - 1
                                            break
                                        except IndexError:
                                            z += 1
                                        except ValueError:
                                            start_l_failure = True
                                            break
                                    # except IndexError:
                                    #     print(node)
                                    #     print(broken_nodes)
                                    #     print(i-1)
                                    #     print(broken_nodes[i-1])
                                    #     exit()
                                    if start_l_failure:
                                        break
                                    start_offset = int(broken_nodes[i-(1+z)][2])
                                    end_l = int(broken_nodes[start_back_search][1]) - 1
                                    end_offset = int(broken_nodes[start_back_search][2]) + len(broken_nodes[start_back_search][0]) + (num_rs-level)
                                    if start_l == end_l:
                                        methods.append([start_l, end_l, start_offset, end_offset])
                                    else:
                                        start_offsets = []
                                        end_offsets = []
                                        start_offsets.append(start_offset)
                                        end_offsets.append(len(lines[start_l]) - 1)
                                        for x in lines[start_l+1:end_l]:
                                            start_offsets.append(len(x) - len(x.strip()) - 1)
                                            end_offsets.append(len(x))
                                        start_offsets.append(len(lines[end_l]) - len(lines[end_l].strip()) - 1)
                                        end_offsets.append(end_offset)
                                        methods.append([start_l, end_l, start_offsets, end_offsets])
                                    lpc = 0
                                    rpc = 0
                                    for iy, y in enumerate(broken_nodes):
                                        if y == '(':
                                            lpc += 1
                                            for z in broken_nodes[iy+1:]:
                                                if isinstance(z, list):
                                                    parameters.append([int(z[1])-1, int(z[2]), int(z[2]) + len(z[0])])
                                                elif z == '(':
                                                    lpc += 1
                                                elif z == ')':
                                                    rpc += 1
                                                if lpc == rpc:
                                                    break
                                            break
                                    break
                                elif broken_nodes[start_back_search] == '(':
                                    try:
                                        methods.append([int(broken_nodes[i-1][1])-1,
                                                        int(broken_nodes[i-1][1])-1,
                                                        int(broken_nodes[i-1][2]),
                                                        int(broken_nodes[i-1][2]) + len(broken_nodes[i-1][0]) + 2])
                                    except IndexError:
                                        pass
                                    break
                                else:
                                    start_back_search -= 1
                            break
                #print('///////////////')
            try:
                get_methods_and_args(one.children, lines)
            except AttributeError:
                pass

    get_methods_and_args(p_children, f_lines)
    return [methods, parameters]
