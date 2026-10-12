"""Check native ladder placement/orientation independently of the writer."""
from pathlib import Path
import math,struct
root=Path(__file__).resolve().parents[1]
data=(root/'GameData/RoosterWorksStationModules/Models/RW_HAB_250.mu').read_bytes()
name=b'RW_HAB250_EVA_Ladder';marker=bytes([len(name)])+name
assert data.count(marker)==1
i=data.index(marker)+len(marker)
x,y,z,qx,qy,qz,qw,sx,sy,sz=struct.unpack_from('<10f',data,i);i+=40
assert struct.unpack_from('<i',data,i)[0]==24;i+=4
assert data[i:i+7]==b'\x06Ladder';i+=7
assert struct.unpack_from('<iiB',data,i)==(21,28,1);i+=9
width,height,depth,cx,cy,cz=struct.unpack_from('<6f',data,i)
assert (sx,sy,sz)==(1,1,1) and (cx,cy,cz)==(0,0,0)
assert abs(math.hypot(x,z)-1.43)<1e-5 and abs(y+.64875)<1e-5
assert abs(width-.86)<1e-5 and abs(height-1.64)<1e-5 and abs(depth-.70)<1e-5
forward=(2*(qx*qz+qw*qy),2*(qy*qz-qw*qx),1-2*(qx*qx+qy*qy))
assert forward[0]*x+forward[2]*z < -1.429, 'Kerbal must face into hull'
assert abs(qx)+abs(qz)<1e-6, 'Local +Y must remain climb-up'
# Trigger contains the unchanged airlock center, enabling stock auto-grab.
h=b'RW_HAB250_EVA_Airlock';j=data.index(bytes([len(h)])+h)+len(h)+1
assert max(abs(a-b) for a,b in zip((x,y,z),struct.unpack_from('<3f',data,j)))<1e-6
print('PASS native Ladder tag, trigger, layer 21, inward facing, vertical axis, exit overlap')
print('NOTE stock auto-grab, climbing and boarding require in-game confirmation')
