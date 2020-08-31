# khu-crawler
<kic-crawler 자매품>

＊<b>기능:</b> 경희대 공식 누리집에 게시되는 공지 사항들을 자동으로 수집해서 텔레그램 채널로 전송해줍니다.<br>

＊<b>특장:</b><br>
&nbsp;&nbsp;&nbsp;1. <i>빠르다.</i> - 현재 자체 호스팅 중인 서버에서 1분 간격으로 신규 공지 사항을 크롤링하도록 설정함.<br>
&nbsp;&nbsp;&nbsp;2. <i>편리하다.</i> - 한 번 원하는 채널에 가입하면 이후부터는 학교 누리집을 방문하지 않고도 공지 사항들을 준실시간으로 확인 가능.<br>
&nbsp;&nbsp;&nbsp;3. <i>정확하다.</i> - 학생들이 직접 학교 누리집을 방문하기가 귀찮아서 에X리X임과 같은 커뮤니티 정보 게시판에 의존하는 경우가 많음. 본 크롤러는 학교 누리집에서 직접 정보를 수집해서 전파하기에 여느 수단보다도 학교관련 정보가 정확함.<br>

＊<b>사용법:</b><br>
   &nbsp;&nbsp;&nbsp;♣<i>일반 이용자(학교 공지 사항만 수신 희망):</i><br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. 텔레그램 가입<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. 추적하고 싶은 공지 게시판에 따라 채널 가입<br>
         &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;일반 - https://t.me/khu_notices_general  /  @khu_notices_general<br>
         &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;학사 - https://t.me/khu_notices_undergraduate  /  @khu_notices_undergraduate<br>
         &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;장학 - https://t.me/khu_notices_scholarships  /  @khu_notices_scholarships<br>
         &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;교내학점교류 - https://t.me/khu_notices_credex  / @khu_notices_credex<br>
         &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;행사 - https://t.me/khu_notices_events  / @khu_notices_events<br>
     
   &nbsp;&nbsp;&nbsp;♣<i>개발자(자체 서버에 탑재 또는 코드 이용 희망):</i><br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. 텔레그램 가입<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. 코드 상 존재하는 각종 경로, API 키 또는 토큰, 그리고 텔레그램 채널과 봇을 알맞게 기입 및 생성<br>
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3. Linux 계열 서버에서 코드 실행 시 crontab, Windows 계열 서버에서는 작업 스케쥴러 등의 반복 실행 메커니즘을 활용해 원하는 주기로 크롤링을 실행<br>

＊<b>동기:</b><br>
&nbsp;&nbsp;&nbsp;♣'사람에게 도움이 된다'는 코딩의 본질을 할 수 있는 범위 안에서 조금이나마 실천해보고 싶었음.<br>
&nbsp;&nbsp;&nbsp;♣2020년 여름방학 때 같은 학과 학우들을 대상으로 하는 'kic-crawler'를 완성하고 나서 보다 많은 학우들에게 편익이 돌아가는 프로젝트를 진행해보고 싶었음.<br>

＊<b>기타:</b><br>
&nbsp;&nbsp;&nbsp;♣학교 누리집 공지 게시판의 갯수는 'khu-crawler'에서 다루는 다섯 개 말고도 두 개(시간표 변경, e-커뮤니티)가 더 존재함. 하지만, '시간표 변경' 게시판은 2018년 09월 05일을 마지막으로 약 1년 동안 신규 공지가 탑재되지 않아 유명무실해진 것으로 판단했고, 'e-커뮤니티' 게시판은 공지 게시판보다는 다른 웹사이트로 이어지는 링크로서의 기능에 더 가깝다고 판단했음. 이에 위 두 개 게시판은 크롤링 대상에서 제외함..<br>
&nbsp;&nbsp;&nbsp;♣텔레그램을 매체로 선택한 이유는 다른 여느 메신저 보다도 API와 관련 모듈 개발이 활발하다고 생각해서임. 2018년 기준 리얼미터 통계에 따르면, 텔레그램이 한국 인기 1위 메시저보다는 못하지만 2위를 차지하고 있음.<br>
&nbsp;&nbsp;&nbsp;♣크롤링 주기는 학교 담당 부서들과의 상의 하 30분(수강 신청 등 특수 사례에도 문제없는 정도)으로 설정함.<br>
&nbsp;&nbsp;&nbsp;♣적어도 본인의 재학 기간 동안은 자체 서버에서 호스팅 및 운용할 계획임. 이후 계획은 이용률을 봐서 판단할 예정임.<br>
&nbsp;&nbsp;&nbsp;♣본 작품은 개발자 본인이 선의로서 개발한 작품이고 최선을 다해서 유지관리에 임하겠지만, 본 작품은 각 개인이 각자의 책임 하 이용해야 하며 이로 인해 발생할 수 있는 어떠한 피해에 대해서도 개발자는 책임질 수 없음.<br>


＊<b>모듈 별 역할:</b><br>
   &nbsp;&nbsp;&nbsp;♣khu_crawler - 각종 모듈의 도움을 받아 학교 누리집의 다섯 개 공지 게시판(일반, 학사, 장학, 교내학점교류, 행사)을 크롤링한 뒤 수집한 내용을 텔레그램 봇을 통해 각 채널에 전파.<br>
   &nbsp;&nbsp;&nbsp;♣dbman - sqlite3을 이용한 최신 공지 사항의 관리.<br>
   &nbsp;&nbsp;&nbsp;♣bitly - URL 단축 서비스인 'Bitly'(bitly.com)의 API를 통해 수집한 공지 사항의 URL 단축.<br>
