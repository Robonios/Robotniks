var summaryData = null, roundsData = null;
var currentPeriod = 'Q1_2026';
var trendsChart = null, sectorChart = null;
var sectorColors = {
  'Semiconductors':'#F5D921','Robotics':'#3B82F6','Space':'#94A3B8',
  'Cross-Stack':'#22C55E','Materials':'#FB923C'
};
var sectorPillCls = {
  'Semiconductors':'sp-semi','Robotics':'sp-robo','Space':'sp-space',
  'Cross-Stack':'sp-cross','Materials':'sp-mat'
};

function fmtM(n){if(!n)return'n/d';if(n>=1000)return'$'+(n/1000).toFixed(1)+'B';return'$'+n.toLocaleString()+'M'}
function fmtDate(d){if(!d)return'\u2014';var p=d.split('-');var months=['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];return p[2].replace(/^0/,'')+'-'+months[parseInt(p[1])]+'-'+p[0].slice(2)}

function esc(s){var d=document.createElement('div');d.textContent=s||'';return d.innerHTML}

async function init(){
  var cb='?v='+Date.now();
  var [sResp,rResp]=await Promise.all([fetch('data/funding/summary.json'+cb),fetch('data/funding/rounds.json'+cb)]);
  summaryData=await sResp.json();
  roundsData=(await rResp.json()).rounds;
  renderAll();
  buildGatedTables();
}

function setPeriod(btn){
  document.querySelectorAll('.time-btn').forEach(function(b){b.classList.remove('active')});
  btn.classList.add('active');
  currentPeriod=btn.dataset.period;
  renderAll();
}

function setTab(tab,btn){
  document.querySelectorAll('.fund-tab').forEach(function(b){b.classList.remove('active')});
  btn.classList.add('active');
  ['overview','rounds','investors','funds'].forEach(function(t){
    document.getElementById('tab-'+t).style.display=t===tab?'':'none';
  });
}

function renderAll(){
  if(!summaryData)return;
  var p=summaryData.periods[currentPeriod];
  var q1=summaryData.periods.Q1_2026;
  var q4=summaryData.periods.Q4_2025;
  var showChange=currentPeriod==='Q1_2026';

  var chg=function(curr,prev){
    if(!showChange||!prev)return'';
    var pct=((curr-prev)/prev*100).toFixed(0);
    var cls=pct>=0?'v-green':'v-red';
    return' <span class="metric-change '+cls+'">'+(pct>=0?'+':'')+pct+'%<\/span>';
  };
  var cards=[
    {label:'Capital Raised',value:fmtM(p.total_capital_m),change:chg(q1.total_capital_m,q4.total_capital_m)},
    {label:'Number of Rounds',value:p.num_rounds,change:chg(q1.num_rounds,q4.num_rounds)},
    {label:'Avg Deal Size',value:fmtM(p.avg_deal_size_m),change:chg(q1.avg_deal_size_m,q4.avg_deal_size_m)},
    {label:'Most Active Sector',value:p.most_active_sector,sub:p.sector_breakdown[p.most_active_sector]?p.sector_breakdown[p.most_active_sector].rounds+' rounds':''},
    {label:'Largest Round',value:p.largest_round?esc(p.largest_round.company):'\u2014',sub:p.largest_round?fmtM(p.largest_round.amount_m):''},
    {label:'Top Investor',value:summaryData.top_investors[0]?esc(summaryData.top_investors[0].name):'\u2014',sub:summaryData.top_investors[0]?summaryData.top_investors[0].deals+' deals':''}
  ];
  var mg=document.getElementById('metrics-grid');
  mg.innerHTML='';
  cards.forEach(function(c){
    var d=document.createElement('div');d.className='metric-card';
    d.innerHTML='<div class="metric-label">'+c.label+'<\/div><div class="metric-value">'+c.value+(c.change||'')+'<\/div>'+(c.sub?'<div class="metric-sub">'+c.sub+'<\/div>':'');
    mg.appendChild(d);
  });

  // Top 10 Rounds
  var filtered=currentPeriod==='6M'?summaryData.top_rounds:summaryData.top_rounds.filter(function(r){
    if(currentPeriod==='Q1_2026')return r.date&&r.date>='2026-01-01';
    return r.date&&r.date<'2026-01-01';
  });
  filtered=filtered.slice(0,10);
  var tbody=document.getElementById('top-rounds-body');
  tbody.innerHTML='';
  filtered.forEach(function(r,i){
    var tr=document.createElement('tr');
    tr.innerHTML='<td style="color:#5A6178">'+(i+1)+'<\/td><td style="font-weight:600">'+esc(r.company)+'<\/td><td><span class="sector-pill '+(sectorPillCls[r.sector]||'')+'">'+esc(r.sector)+'<\/span><\/td><td>'+esc(r.round)+'<\/td><td class="r" style="font-weight:600">'+fmtM(r.amount_m)+'<\/td><td style="color:#5A6178">'+fmtDate(r.date)+'<\/td>';
    tbody.appendChild(tr);
  });

  renderSectorChart(p);
  renderTrendsChart(p);
  renderTopInvestors();
  renderStageDistribution(p);
  renderNotable(p);
}

function renderTrendsChart(p){
  var months=currentPeriod==='Q1_2026'?['Jan-26','Feb-26','Mar-26']:currentPeriod==='Q4_2025'?['Oct-25','Nov-25','Dec-25']:['Oct-25','Nov-25','Dec-25','Jan-26','Feb-26','Mar-26'];
  var sectors=['Semiconductors','Robotics','Space','Cross-Stack','Materials'];
  var datasets=sectors.map(function(s){return{
    label:s,backgroundColor:sectorColors[s],
    data:months.map(function(m){return(p.monthly_by_sector[m]&&p.monthly_by_sector[m][s])?Math.round(p.monthly_by_sector[m][s]):0})
  }});
  if(trendsChart)trendsChart.destroy();
  trendsChart=new Chart(document.getElementById('trends-chart'),{
    type:'bar',
    data:{labels:months,datasets:datasets},
    options:{responsive:true,plugins:{legend:{display:true,position:'bottom',labels:{color:'#8B92A5',font:{family:'Roboto Mono',size:9},boxWidth:10,padding:8}}},scales:{x:{stacked:true,ticks:{color:'#5A6178',font:{family:'Roboto Mono',size:9}},grid:{color:'#1E2330'}},y:{stacked:true,ticks:{color:'#5A6178',font:{family:'Roboto Mono',size:9},callback:function(v){return'$'+v.toLocaleString()+'M'}},grid:{color:'#1E2330'}}}}
  });
}

function renderSectorChart(p){
  var sectors=Object.keys(p.sector_breakdown);
  var vals=sectors.map(function(s){return p.sector_breakdown[s].capital_m});
  var total=vals.reduce(function(a,b){return a+b},0);
  if(sectorChart)sectorChart.destroy();
  sectorChart=new Chart(document.getElementById('sector-chart'),{
    type:'doughnut',
    data:{labels:sectors,datasets:[{data:vals,backgroundColor:sectors.map(function(s){return sectorColors[s]}),borderWidth:0}]},
    options:{responsive:true,cutout:'60%',plugins:{legend:{display:true,position:'bottom',labels:{color:'#8B92A5',font:{family:'Roboto Mono',size:9},boxWidth:10,padding:6,generateLabels:function(chart){return chart.data.labels.map(function(l,i){var v=chart.data.datasets[0].data[i];var pct=total>0?(v/total*100).toFixed(0)+'%':'0%';return{text:l+' '+pct+' ('+fmtM(v)+')',fillStyle:chart.data.datasets[0].backgroundColor[i],hidden:false,index:i}})}}}}}
  });
}

function renderTopInvestors(){
  var invs=summaryData.top_investors.slice(0,10);
  var maxDeals=invs.length?invs[0].deals:1;
  var container=document.getElementById('top-investors');
  container.innerHTML='';
  invs.forEach(function(inv){
    var d=document.createElement('div');d.className='inv-bar';
    d.innerHTML='<div class="inv-name" title="'+esc(inv.name)+'">'+esc(inv.name)+'<\/div><div class="inv-fill" style="width:'+Math.round(inv.deals/maxDeals*120)+'px"><\/div><div class="inv-count">'+inv.deals+'<\/div>';
    container.appendChild(d);
  });
}

function renderStageDistribution(p){
  if(!p.stage_breakdown)return;
  var stages=['Seed','Series A','Series B','Series C','Series D+','Other'];
  var stgColors=['#F5D921','#3B82F6','#22C55E','#a78bfa','#ef4444','#5A6178'];
  var maxRounds=Math.max.apply(null,stages.map(function(s){return(p.stage_breakdown[s]?p.stage_breakdown[s].rounds:0)}));
  var container=document.getElementById('stage-dist');
  container.innerHTML='';
  stages.forEach(function(s,i){
    var d=p.stage_breakdown[s]||{rounds:0,capital_m:0};
    var el=document.createElement('div');el.className='stage-row';
    el.innerHTML='<div class="stage-label">'+s+'<\/div><div class="stage-bar" style="width:'+Math.round(d.rounds/maxRounds*100)+'px;background:'+stgColors[i]+'"><\/div><div class="stage-val">'+d.rounds+' ('+fmtM(d.capital_m)+')<\/div>';
    container.appendChild(el);
  });
}

function renderNotable(p){
  var total=p.total_capital_m;
  var rounds=p.num_rounds;
  var mostActive=p.most_active_sector;
  var mostActiveRounds=p.sector_breakdown[mostActive]?p.sector_breakdown[mostActive].rounds:0;
  var megas=summaryData.top_rounds.filter(function(r){return r.amount_m>=500}).length;
  var semiCap=p.sector_breakdown['Semiconductors']?p.sector_breakdown['Semiconductors'].capital_m:0;
  var semiRounds=p.sector_breakdown['Semiconductors']?p.sector_breakdown['Semiconductors'].rounds:0;
  var avgSemi=semiRounds>0?Math.round(semiCap/semiRounds):0;
  var periodLabel=currentPeriod==='6M'?'Q4 2025 and Q1 2026':currentPeriod==='Q1_2026'?'Q1 2026':'Q4 2025';
  document.getElementById('notable-card').innerHTML=
    'Tovarishch, <strong>'+rounds+' frontier stack rounds<\/strong> detected in '+periodLabel+', deploying <strong>'+fmtM(total)+'<\/strong> of capital. '+esc(mostActive)+' dominates deal flow with '+mostActiveRounds+' rounds, but Semiconductors commands the highest average deal size at '+fmtM(avgSemi)+' per round. <strong>'+megas+' mega-rounds<\/strong> exceeding $500M signal deep conviction in frontier compute and physical AI infrastructure. Capital deployment is accelerating quarter-over-quarter.';
}

function buildGatedTables(){
  var rt=document.getElementById('rounds-blur-table');
  var tbl=document.createElement('table');tbl.className='top-table';tbl.style.margin='1rem';
  tbl.innerHTML='<thead><tr><th>Company<\/th><th>Sector<\/th><th>Round<\/th><th class="r">Amount<\/th><th>Lead<\/th><th>Date<\/th><th>Location<\/th><\/tr><\/thead>';
  var tb=document.createElement('tbody');
  roundsData.slice(0,15).forEach(function(r){
    var tr=document.createElement('tr');
    tr.innerHTML='<td>'+esc(r.company)+'<\/td><td>'+esc(r.sector)+'<\/td><td>'+esc(r.round||'')+'<\/td><td class="r">'+(r.amount_m?fmtM(r.amount_m):'n/d')+'<\/td><td>'+esc(r.lead_investors||'\u2014')+'<\/td><td>'+fmtDate(r.date)+'<\/td><td>'+esc(r.location||'\u2014')+'<\/td>';
    tb.appendChild(tr);
  });
  tbl.appendChild(tb);
  rt.appendChild(tbl);

  var it=document.getElementById('investors-blur-table');
  var tbl2=document.createElement('table');tbl2.className='top-table';tbl2.style.margin='1rem';
  tbl2.innerHTML='<thead><tr><th>Investor<\/th><th class="r"># Deals<\/th><th>Sectors<\/th><\/tr><\/thead>';
  var tb2=document.createElement('tbody');
  summaryData.top_investors.slice(0,10).forEach(function(inv){
    var tr=document.createElement('tr');
    tr.innerHTML='<td>'+esc(inv.name)+'<\/td><td class="r">'+inv.deals+'<\/td><td>'+esc(inv.sectors.join(', '))+'<\/td>';
    tb2.appendChild(tr);
  });
  tbl2.appendChild(tb2);
  it.appendChild(tbl2);
}

init();
