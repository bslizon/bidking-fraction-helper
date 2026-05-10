#!/usr/bin/env python3

from decimal import Decimal, InvalidOperation, ROUND_DOWN, ROUND_HALF_UP, ROUND_CEILING


def guess_fractions(x_str, limit, top_k):
    # 参数检查：x_str
    if not isinstance(x_str, str):
        raise ValueError("输入值必须是字符串")

    x_str = x_str.strip()

    if not x_str:
        raise ValueError("输入不能为空")

    try:
        target = Decimal(x_str)
    except InvalidOperation:
        raise ValueError("输入不是合法数字")

    if not target.is_finite():
        raise ValueError("输入不能是 NaN 或 Infinity")

    if target <= 0:
        raise ValueError("输入必须是正数")

    if target.as_tuple().exponent < -2:
        raise ValueError("输入最多只能有小数点后 2 位")

    target = target.quantize(Decimal("0.01"))

    # 参数检查：limit
    if not isinstance(limit, int):
        raise ValueError("limit 必须是整数")

    if limit <= 0:
        raise ValueError("limit 必须大于 0")

    # 参数检查：top_k
    if not isinstance(top_k, int):
        raise ValueError("top_k 必须是整数")

    if top_k <= 0:
        raise ValueError("top_k 必须大于 0")

    results = []

    for a in range(1, limit + 1):
        for b in range(1, limit + 1):
            value = Decimal(a) / Decimal(b)

            truncated = value.quantize(Decimal("0.01"), rounding=ROUND_DOWN)
            rounded = value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            ceiled = value.quantize(Decimal("0.01"), rounding=ROUND_CEILING)

            matched_methods = []

            if truncated == target:
                matched_methods.append("舍去")

            if rounded == target:
                matched_methods.append("四舍五入")

            if ceiled == target:
                matched_methods.append("进一法")

            if matched_methods:
                error = abs(value - target)
                is_priority = "舍去" in matched_methods

                results.append({
                    "a": a,
                    "b": b,
                    "value": value,
                    "truncated": truncated,
                    "rounded": rounded,
                    "ceiled": ceiled,
                    "error": error,
                    "methods": matched_methods,
                    "is_priority": is_priority,
                })

    # 排序：
    # 1. 截断/舍去命中的优先
    # 2. 分子+分母越小越靠前
    # 3. 分子越小越靠前
    # 4. 分母越小越靠前
    results.sort(key=lambda item: (
        not item["is_priority"],
        item["a"] + item["b"],
        item["a"],
        item["b"]
    ))

    return results[:top_k]


def main():
    limit = 100
    top_k = 30

    # 参数检查：固定参数
    if not isinstance(limit, int):
        print("参数错误: limit 必须是整数")
        return

    if limit <= 0:
        print("参数错误: limit 必须大于 0")
        return

    if not isinstance(top_k, int):
        print("参数错误: top_k 必须是整数")
        return

    if top_k <= 0:
        print("参数错误: top_k 必须大于 0")
        return

    print("参数:")
    print(f"limit = {limit}")
    print(f"top_k = {top_k}")
    print("备注：历史数据存在过 3.81 验证，因此命中截断/舍去规则的结果标记为【优先考虑】。")

    while True:
        x_str = input("\n请输入一个小数，最多保留小数点后 2 位；直接回车或输入 q 退出: ").strip()

        if x_str == "" or x_str.lower() in {"q", "quit", "exit"}:
            print("已退出")
            break

        try:
            results = guess_fractions(
                x_str=x_str,
                limit=limit,
                top_k=top_k
            )
        except ValueError as e:
            print(f"输入错误: {e}")
            continue

        if not results:
            print("没有找到符合条件的组合")
            continue

        print(f"\n前 {top_k} 个匹配小数点后 2 位，且截断结果优先考虑的组合:")

        for i, item in enumerate(results, start=1):
            methods = "、".join(item["methods"])
            priority_text = "【优先考虑：疑似截断】" if item["is_priority"] else ""

            print(
                f"{i:2d}. "
                f"{item['a']:2d} / {item['b']:2d} = {item['value']:.12f}, "
                f"舍去={item['truncated']}, "
                f"四舍五入={item['rounded']}, "
                f"进一法={item['ceiled']}, "
                f"匹配方式={methods}, "
                f"误差={item['error']} "
                f"{priority_text}"
            )

        summary = ", ".join(
            f"{item['a']}/{item['b']}"
            for item in results
        )

        print("\n汇总:")
        print(summary)

        priority_summary = ", ".join(
            f"{item['a']}/{item['b']}"
            for item in results
            if item["is_priority"]
        )

        if priority_summary:
            print("\n优先考虑汇总:")
            print(priority_summary)
            print("说明：这些组合命中截断/舍去规则；历史数据存在过 3.81 验证，因此优先考虑。")


if __name__ == "__main__":
    main()