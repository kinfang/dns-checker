# app.py

from flask import Flask, render_template, request, jsonify
import dns.resolver
import dns.exception

app = Flask(__name__)

# 定义一个函数来查询单个服务器的DNS解析结果
def get_dns_result(domain, dns_server):
    """
    对指定的DNS服务器查询指定域名。
    返回解析结果的列表 (如 ['1.1.1.1', '2.2.2.2']) 或 错误信息。
    """
    try:
        # 创建一个自定义解析器，指定要查询的DNS服务器IP
        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = [dns_server]
        # 设置超时时间（例如 5 秒）
        resolver.timeout = 5
        resolver.lifetime = 5
        
        # 默认查询A记录（IPv4地址）
        answers = resolver.resolve(domain, 'A')
        
        # 将解析结果转换为IP地址字符串列表
        results = [str(r) for r in answers]
        
        # 排序后返回，确保结果如 [ '1.1.1.1', '2.2.2.2' ] 和 [ '2.2.2.2', '1.1.1.1' ] 也能被视为一致
        return sorted(results)

    except dns.exception.Timeout:
        return ["超时"]
    except dns.resolver.NoAnswer:
        return ["无解析记录 (No Answer)"]
    except dns.resolver.NXDOMAIN:
        return ["域名不存在 (NXDOMAIN)"]
    except Exception as e:
        # 捕获其他可能的错误，如服务器无法访问
        return [f"查询错误: {e}"]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 1. 获取用户输入
        domain = request.form['domain'].strip()
        # 将用户输入的服务器IP地址按行分割，并过滤空行
        servers_input = request.form['dns_servers']
        dns_servers = [s.strip() for s in servers_input.split('\n') if s.strip()]

        final_results = []
        all_results = {}

        # 2. 遍历服务器并执行查询
        for server in dns_servers:
            result_list = get_dns_result(domain, server)
            # 将结果列表转换为一个字符串，方便后续比较
            result_str = " | ".join(result_list)
            
            # 存储所有结果字符串，用于检查一致性
            all_results[server] = result_str
            
            # 初始状态设为 'consistent'
            final_results.append({
                'server': server,
                'result': result_str,
                'status': 'consistent' 
            })

        # 3. 比较所有结果
        unique_results = set(all_results.values())
        
        if len(unique_results) > 1:
            # 存在不一致的结果
            
            # 找到出现次数最多的结果，作为“基准”
            result_counts = {}
            for res_str in all_results.values():
                result_counts[res_str] = result_counts.get(res_str, 0) + 1
            
            # 最多出现的结果字符串（用作比较的基准）
            # 这里的逻辑可以简化为：只要 unique_results.size > 1，所有结果都视为不一致（即每个都可能是"错误的"）
            # 另一种更友好的方式：将所有不等于 "基准结果" 的标记为红色
            
            # 为了简单起见，我们直接标记所有不一致的结果
            # 这里我们不找基准，只要结果集大小 > 1，所有结果都将参与一致性比较
            
            for item in final_results:
                # 任何结果与唯一的那个结果（如果只有一个）不符，或结果集大于1时，都视为不一致
                if len(unique_results) > 1:
                    # 只要存在多于一个不同的解析结果，所有结果都标记为 inconsistent
                    # 更好的做法是，标记与最常见结果不同的那些，但简单起见，我们让用户自己判断
                    item['status'] = 'inconsistent'
                
        # 4. 返回结果到前端
        return render_template('index.html', results=final_results, domain=domain, dns_servers=servers_input)

    # GET 请求时显示初始页面
    return render_template('index.html', results=None)

if __name__ == '__main__':
    # 运行Flask应用
    # app.run(host='0.0.0.0', port=5000, debug=True)
    pass
