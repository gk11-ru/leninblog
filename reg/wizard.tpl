<h1>Создание блога</h1>
<form method="POST">
<p><b>Бренд, логотип</b>. Это заголовок сайта.</p>
<input type="text" name="brand" value="{{conf.BRAND}}">

<hr>
<p><b>Таглайн</b>. Это девиз сайта. Маленькая подпись под логотипом.</p>
<input type="text" name="tagline" value="{{conf.TAGLINE}}">

<hr>
<p><b>Блог по умолчанию</b>. Название идентификатора блога. По стандарту он должен быть из маленьких латинских букв и <b>обязательно содержать точку!</b>
Вторая колонка задаёт описание блога.</p>
<input type="text" name="ea" value="{{conf.EA}}"> <input type="text" name="eadesc" value="Это очень нужный блог!">

<hr>
<p><b>Улица</b>. Средство внутренней адресации. Пишите сюда только маленькие латинские буквы!</p>
<input type="text" name="addr" value="{{conf.ADDR}}">

<hr>
<p><b>URL</b>. Полный и корректный адрес сайта. Без конечного слеша, но с указанием протокола. Пример верного указания: <b>http://192.168.0.1:13014</b></p>
<input type="text" name="url" value="{{conf.URL}}">

<hr>
<p><b>Описание</b>. Краткое описание вашего сайта</p>
<input type="text" name="desc" value="{{conf.DESC}}">

<hr>
<p><b>admikey</b>. Код доступа, позволяет включать режим удаления сообщений. Режим включается в профиле, при введении этого кода.</p>
<input type="password" name="akey" value="">


<p><input type="submit" value="Создать сайт"></p>

</form>