hexstr = "e481e8e6bfb936f08b3cf5b87a4ce86dd423ab47a1e740ce000499b4455d3ed4e3e2e5e59b4a238738e4fcb2bcc9d21aa7147124aa19f25640fd169bd37d7c3fa0a0e1a41855f636bd956196442ea53d428c448da0f96b0c943a4de79e04d0983689cfda06436b70ace5ef03320e82d41c9692ff09529343c3ddeea7c3390e1d4727c0ea02699e7a3dd39a6603a57c9904b17ea9deb47997f8b3f5df1788d61ebf4d9cd341708a620c8f7a0be87da023e15922ab02d9fb5d58c95c311f5b5b74927c5f1c61977b1e70aef94fe6e6c1186b7218841fed3d366ff63d2871047d08f6aed8c2b59c3ed98430cabbd5616c79224b4297a7ac07854a289100670e41ca"

data = bytes.fromhex(hexstr)
print("total len:", len(data))
print("first 64 (public frame):", data[:64])
print()
leaked = data[64:]
print("leaked bytes len:", len(leaked))
print("leaked raw:", leaked)
print()
print("leaked ascii (errors replaced):", leaked.decode('latin1'))
