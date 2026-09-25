body = (
    r"""=H],=P)ts(;Pfe\S=!EVXK\:%CM[CmH$6*5Wi<"IY()&,L9RtlK8PPA[CWo\eY04?IaZ>hcH+&Xa"""
    r"""4H.&e'm67i83%If&brYQJ:6WgYhOkj6-'.]_D0cm-s`6pT+;apAkEteG"""
)
print("len:", len(body))
codes = [ord(c) for c in body]
print("min ord:", min(codes), chr(min(codes)))
print("max ord:", max(codes), chr(max(codes)))
print("distinct chars:", len(set(body)))
print(sorted(set(body)))
