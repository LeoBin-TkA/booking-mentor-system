const API = location.origin; // ví dụ http://192.168.0.6:6868

// ===== Utils =====
const $ = (sel) => document.querySelector(sel);
function toast(msg, type='info'){
  const el = $('#toast');
  if(!el) return;
  el.textContent = msg;
  el.style.background = (type==='ok') ? '#157347' : (type==='warn'? '#a96a00' : (type==='err'? '#9d2d2d' : '#111c33'));
  el.classList.add('show');
  setTimeout(()=> el.classList.remove('show'), 2200);
}
function setOut(obj){ $('#out').textContent = (typeof obj === 'string') ? obj : JSON.stringify(obj, null, 2); }

// Simple theme toggle (prefers-color-scheme vẫn hoạt động, đây chỉ là thủ công)
$('#toggleTheme')?.addEventListener('click', () => {
  const dark = document.documentElement.classList.toggle('dark');
  toast(`Đã chuyển chế độ ${dark ? 'tối' : 'sáng'}`);
});

// ===== Demo Data mapping (dùng /todos tạm như mentor) =====
// Khi có API thật:
//   GET  /mentors            -> danh sách mentor
//   GET  /slots?mentor_id=ID -> slot theo mentor
//   POST /bookings           -> body = { mentor_id, start_time, student_name, note }
async function loadMentors(){
  const res = await fetch(`${API}/todos/`);
  if(!res.ok) throw new Error(`GET /todos/ failed: ${res.status}`);
  const list = await res.json();

  // map tạm thành mentor (id, name, bio)
  const mentors = list.map((t,i)=> ({
    id: t.id,
    name: t.title || `Mentor #${t.id}`,
    bio: t.description || `Chuyên môn: Tổng hợp | Kinh nghiệm: ${2 + (i%4)} năm | Đánh giá: ${(4 + (i%2)*.5).toFixed(1)}/5`
  }));

  const sel = $('#mentorSelect');
  sel.innerHTML = mentors.map(m => `<option value="${m.id}">${m.name}</option>`).join('');
  sel.dataset.cache = JSON.stringify(mentors);
  updateMentorInfo();
}

function updateMentorInfo(){
  const sel = $('#mentorSelect');
  const info = $('#mentorInfo');
  if(!sel.value){ info.innerHTML = "<p>Chọn mentor để xem mô tả.</p>"; return; }
  const mentors = JSON.parse(sel.dataset.cache || '[]');
  const m = mentors.find(x=> String(x.id) === String(sel.value));
  if(!m){ info.innerHTML = "<p>Chọn mentor để xem mô tả.</p>"; return; }
  info.innerHTML = `
    <strong>${m.name}</strong>
    <p>${m.bio}</p>
  `;
}

async function loadSlots(){
  // Demo tạo 6 slot trong 3 ngày tới
  const now = new Date();
  const mk = (d,h) => new Date(d.getFullYear(), d.getMonth(), d.getDate(), h, 0);
  const a = [ mk(now, 9), mk(now, 14), mk(new Date(now.getTime()+86400000), 10), mk(new Date(now.getTime()+86400000), 15), mk(new Date(now.getTime()+172800000), 9), mk(new Date(now.getTime()+172800000), 13) ];
  const fmtVal = d => d.toISOString().slice(0,16); // yyyy-MM-ddTHH:mm
  const fmtTxt = d => d.toLocaleString();

  const sel = $('#slotSelect');
  sel.innerHTML = a.map(d => `<option value="${fmtVal(d)}">${fmtTxt(d)}</option>`).join('');
}

async function book(){
  const mentorId = $('#mentorSelect').value;
  const slot = $('#slotSelect').value;
  const name = $('#studentName').value.trim();
  const note = $('#note').value.trim();

  if(!mentorId){ toast('Vui lòng chọn mentor', 'warn'); return; }
  if(!slot){ toast('Vui lòng chọn khung giờ', 'warn'); return; }
  if(!name){ toast('Vui lòng nhập họ tên', 'warn'); return; }

  // Demo: POST /todos để test end-to-end
  try{
    const res = await fetch(`${API}/todos/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: `Booking: ${name} | ${slot} | mentor#${mentorId}${note ? ` | ${note}` : ''}` })
    });
    const data = await res.json();
    if(!res.ok) throw new Error(data?.message || `Lỗi ${res.status}`);

    setOut(data);
    toast('Đặt lịch (demo) thành công!', 'ok');
  }catch(err){
    setOut(String(err));
    toast('Đặt lịch thất bại', 'err');
  }
}

function clearForm(){
  $('#studentName').value = '';
  $('#note').value = '';
  $('#out').textContent = 'Chưa có dữ liệu.';
  toast('Đã xoá nội dung');
}

async function copyOut(){
  try{
    await navigator.clipboard.writeText($('#out').textContent || '');
    toast('Đã copy kết quả', 'ok');
  }catch(_){
    toast('Copy chưa được hỗ trợ', 'warn');
  }
}

// ===== Init =====
document.addEventListener('DOMContentLoaded', async () => {
  try{
    await loadMentors();
    await loadSlots();
  }catch(e){
    setOut(String(e));
    toast('Không tải được dữ liệu', 'err');
  }
  $('#mentorSelect').addEventListener('change', updateMentorInfo);
  $('#refreshMentors').addEventListener('click', loadMentors);
  $('#bookBtn').addEventListener('click', book);
  $('#clearBtn').addEventListener('click', clearForm);
  $('#copyBtn').addEventListener('click', copyOut);
});
