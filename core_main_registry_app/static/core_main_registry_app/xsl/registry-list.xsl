<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0"
	xmlns:nr="http://schema.nist.gov/xml/res-md/1.0wd-02-2017"
    xmlns:exsl="http://exslt.org/common"
    exclude-result-prefixes="exsl">
	<xsl:output method="html" indent="yes" encoding="UTF-8" />

	<xsl:template match="/">
		<div class="white-bg">
			<xsl:variable name="title"  select="//nr:Resource/nr:identity/nr:title"/>
			<xsl:text disable-output-escaping="yes">&lt;a class="title" href="</xsl:text>
			<xsl:text disable-output-escaping="yes">{{ result.detail_url }}</xsl:text>
			<xsl:text disable-output-escaping="yes">" &gt;</xsl:text>
				<xsl:choose>
					<xsl:when test="$title!=''">
						<strong><xsl:value-of select="$title"/></strong>
					</xsl:when>
					<xsl:otherwise>
						<strong class="italic">Untitled</strong>
					</xsl:otherwise>
				</xsl:choose>
			<xsl:text disable-output-escaping="yes">&lt;/a&gt;</xsl:text>
			<div class="black">
                <xsl:variable name="creatorList">
                    <xsl:for-each select="//nr:Resource/nr:providers/nr:creator">
                        <creator>
                            <xsl:value-of select="./nr:name"/>
                            <xsl:variable name="orga" select="./nr:affiliation" />
                            <xsl:if test="$orga!=''">, <xsl:value-of select="$orga"/></xsl:if>
                        </creator>
                    </xsl:for-each>
                </xsl:variable>

                <xsl:variable name="creators" select="exsl:node-set($creatorList)/creator" />

				<xsl:call-template name="join">
					<xsl:with-param name="list" select="$creators" />
					<xsl:with-param name="separator" select="', '" />
				</xsl:call-template>

				<xsl:variable name="publisher" select="//nr:Resource/nr:providers/nr:publisher"/>
				<xsl:if test="( ($creators!='') and ($publisher!='') )">
					<xsl:text> - </xsl:text>
				</xsl:if>
				<xsl:value-of select="$publisher"/>
			</div>
			<xsl:variable name="url" select="//nr:Resource/nr:content/nr:landingPage" />
			<a target="_blank" rel="noopener noreferrer" href="{$url}"><xsl:value-of select="$url"/></a>
			<xsl:variable name="idw">{{ result.detail_url|slice:'-24:' }}</xsl:variable>
			<a data-toggle="collapse" data-target="#{$idw}"
			  aria-expanded="false" aria-controls="{$idw}" class="collapsed">
				<i class="fas fa-chevron-up" />
				<i class="fas fa-chevron-down" />
			</a>
			<div class="collapseXSLT collapse" id="{$idw}">
					<xsl:apply-templates select="//*[not(*)]"/>
					<!--<xsl:variable name="terms" select="//nr:Resource/nr:access/nr:policy/nr:terms" />-->
					<!--<xsl:if test="$terms!=''">-->
						<!--<xsl:text>Terms: </xsl:text>-->
						<!--<xsl:value-of select="$terms"/>-->
						<!--<br/>-->
					<!--</xsl:if>-->
			</div>
			<xsl:variable name="subject" select="//nr:Resource/nr:content/nr:subject" />
			<xsl:if test="$subject!=''">
				<div class="keywords">
					<xsl:text>Subject keyword(s): </xsl:text>
					<xsl:call-template name="join">
						<xsl:with-param name="list" select="$subject" />
						<xsl:with-param name="separator" select="', '" />
					</xsl:call-template>
				</div>
			</xsl:if>
			<div class="black">
				<p class="description">
					<xsl:value-of select="//nr:Resource/nr:content/nr:description"/>
				</p>
			</div>
			<br/>
		</div>
	</xsl:template>

	<xsl:template name="join">
		<xsl:param name="list" />
		<xsl:param name="separator"/>

		<xsl:for-each select="$list">
			<xsl:value-of select="." />
			<xsl:if test="position() != last()">
				<xsl:value-of select="$separator" />
			</xsl:if>
		</xsl:for-each>
	</xsl:template>

	<xsl:template match="//*[not(*)]">
		<xsl:variable name="name" select="name(.)" />
		<xsl:variable name="value" select="." />
		<xsl:variable name="arg" select="@type" />
		<xsl:if test="( (contains($name, 'URL')) or (starts-with($value, 'https://')) or (starts-with($value, 'http://')) )">
			<xsl:if test="$value!=''">
				<xsl:value-of select="$name"/>
				<xsl:text>: </xsl:text>
				<a target="_blank" rel="noopener noreferrer" href="{$value}"><xsl:value-of select="$value"/></a>
				<br/>
			</xsl:if>
		</xsl:if>
	</xsl:template>

</xsl:stylesheet>
